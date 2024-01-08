#include <srldrvce.h>

#include <debug.h>
#include <keypadc.h>
#include <stdbool.h>
#include <string.h>
#include <tice.h>
#include <ti/vars.h>

srl_device_t srl;

bool has_srl_device = false;

uint8_t srl_buf[512];

char EOFstr[2] = "\n";

static usb_error_t handle_usb_event(usb_event_t event, void *event_data,
                                    usb_callback_data_t *callback_data __attribute__((unused))) {
    usb_error_t err;
    /* Delegate to srl USB callback */
    if ((err = srl_UsbEventCallback(event, event_data, callback_data)) != USB_SUCCESS)
        return err;
    /* Enable newly connected devices */
    if(event == USB_DEVICE_CONNECTED_EVENT && !(usb_GetRole() & USB_ROLE_DEVICE)) {
        usb_device_t device = event_data;
        printf("device connected\n");
        usb_ResetDevice(device);
    }

    /* Call srl_Open on newly enabled device, if there is not currently a serial device in use */
    if(event == USB_HOST_CONFIGURE_EVENT || (event == USB_DEVICE_ENABLED_EVENT && !(usb_GetRole() & USB_ROLE_DEVICE))) {

        /* If we already have a serial device, ignore the new one */
        if(has_srl_device) return USB_SUCCESS;

        usb_device_t device;
        if(event == USB_HOST_CONFIGURE_EVENT) {
            /* Use the device representing the USB host. */
            device = usb_FindDevice(NULL, NULL, USB_SKIP_HUBS);
            if(device == NULL) return USB_SUCCESS;
        } else {
            /* Use the newly enabled device */
            device = event_data;
        }

        /* Initialize the serial library with the newly attached device */
        srl_error_t error = srl_Open(&srl, device, srl_buf, sizeof srl_buf, SRL_INTERFACE_ANY, 9600);
        if(error) {
            /* Print the error code to the homescreen */
            printf("Error %d initting serial\n", error);
            return USB_SUCCESS;
        }

        printf("serial initialized\n");

        has_srl_device = true;
    }

    if(event == USB_DEVICE_DISCONNECTED_EVENT) {
        usb_device_t device = event_data;
        if(device == srl.dev) {
            printf("device disconnected\n");
            srl_Close(&srl);
            has_srl_device = false;
        }
    }

    return USB_SUCCESS;
}

int blocking_read(void *data, int len) {
    int recv_len = 0;
    do
    { 
        usb_HandleEvents();
        int read_len = srl_Read(&srl, data + recv_len, len - recv_len);
        if (read_len < 0) { return -1; }
        recv_len += read_len;
    } while (recv_len < len);
    return recv_len;
}

int main(void){
    os_ClrHome();
    const usb_standard_descriptors_t *desc = srl_GetCDCStandardDescriptors();
    usb_error_t usb_error = usb_Init(handle_usb_event, NULL, desc, USB_DEFAULT_INIT_FLAGS);
    if(usb_error) {
       usb_Cleanup();
       printf("usb init error %u\n", usb_error);
       do kb_Scan(); while(!kb_IsDown(kb_KeyClear));
       return 1;
    }
    /*Hierboven is handling shit, niet aankomen pls*/

    /*Nu wordt het leuk*/
    char in_buf[] = "     \0";
    char start[7] = "start";
    printf("%s", "Empty in_buf is:");
    printf("%s", in_buf);
    do{
        kb_Scan();
        usb_HandleEvents();
        //srl_Write(&srl, "start", 5);
        if(has_srl_device){
            printf("%s", "Waiting for start");
            if (blocking_read(in_buf, 5) != -1){
                printf("Received, sending str1");
                string_t *input = os_GetStringData(OS_VAR_STR1, NULL);
                srl_Write(&srl, input->data, input->len);
                srl_Write(&srl, EOFstr, sizeof EOFstr);
                if (strcmp(in_buf, start)){
                    srl_Write(&srl, start, 7);
                    srl_Write(&srl, EOFstr, 2);
                    break;
                }
                
            }
        }
        
        kb_Scan();
    }
    while (!kb_IsDown(kb_KeyClear));
    usb_Cleanup();

}