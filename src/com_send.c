#include <srldrvce.h>

#include <debug.h>
#include <keypadc.h>
#include <stdbool.h>
#include <string.h>
#include <tice.h>
#include <ti/vars.h>
#include <ti/tokens.h>
#include <fileioc.h>

srl_device_t srl_send;

bool has_srl_device_send = false;

uint8_t srl_buf_send[512];

static usb_error_t handle_usb_event(usb_event_t event, void *event_data,
                                    usb_callback_data_t *callback_data __attribute__((unused))) {
    usb_error_t err;
    /* Delegate to srl USB callback */
    if ((err = srl_UsbEventCallback(event, event_data, callback_data)) != USB_SUCCESS)
        return err;
    /* Enable newly connected devices */
    if(event == USB_DEVICE_CONNECTED_EVENT && !(usb_GetRole() & USB_ROLE_DEVICE)) {
        usb_device_t device = event_data;
        usb_ResetDevice(device);
    }

    /* Call srl_Open on newly enabled device, if there is not currently a serial device in use */
    if(event == USB_HOST_CONFIGURE_EVENT || (event == USB_DEVICE_ENABLED_EVENT && !(usb_GetRole() & USB_ROLE_DEVICE))) {

        /* If we already have a serial device, ignore the new one */
        if(has_srl_device_send) return USB_SUCCESS;

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
        srl_error_t error = srl_Open(&srl_send, device, srl_buf_send, sizeof srl_buf_send, SRL_INTERFACE_ANY, 9600);
        if(error) {
            /* Print the error code to the homescreen */
            return USB_SUCCESS;
        }


        has_srl_device_send = true;
    }

    if(event == USB_DEVICE_DISCONNECTED_EVENT) {
        usb_device_t device = event_data;
        if(device == srl_send.dev) {
            srl_Close(&srl_send);
            has_srl_device_send = false;
        }
    }

    return USB_SUCCESS;
}

int main_send(void){
    os_ClrHome();
    const usb_standard_descriptors_t *desc = srl_GetCDCStandardDescriptors();
    usb_error_t usb_error = usb_Init(handle_usb_event, NULL, desc, USB_DEFAULT_INIT_FLAGS);
    
    if(usb_error) {
       usb_Cleanup();
       do kb_Scan(); while(!kb_IsDown(kb_KeyClear));
       return 1;
    }
    /*Hierboven is handling shit, niet aankomen pls*/

    /*Nu wordt het leuk*/
    //dit is com_send, dus we sturen alleen STR0
    kb_Scan();
    usb_HandleEvents();
    if(has_srl_device_send){
        char* input[44];
        ti_RclVar(OS_TYPE_STR, OS_VAR_STR0, (void**)&input);
        srl_Write(&srl_send, input, 44);
    }
    else{
        ti_SetVar(OS_TYPE_STR, OS_VAR_STR1, "FAIL (1)");
    }
        
    kb_Scan();
    usb_Cleanup();
    return 0;

}