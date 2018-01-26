Transmit keystrokes to a running vSphere virtual machine via [pyvmomi](https://github.com/vmware/pyvmomi).

Can be used either as a command-line tool directly, or import as a module.


```
usage: send_keys_to_vm.py [-h] [-c C] [--raw-scancode I] [--modifier {shift,alt,meta,ctrl}]
                          [--moref MOREF] [--uuid UUID] [--ip IP]
                          [-v] [--whatif] [--insecure]
                          [--hostname vCenter-Server] [--port 443] [--username USERNAME] [--password PASSWORD]
                          [keys [keys ...]]

```

`./send_keys_to_vm.py a b C ctrl+d --whatif`

```
(vim.vm.UsbScanCodeSpec.KeyEvent) {
   dynamicType = <unset>,
   dynamicProperty = (vmodl.DynamicProperty) [],
   usbHidCode = 262151,
   modifiers = <unset>
}
(vim.vm.UsbScanCodeSpec.KeyEvent) {
   dynamicType = <unset>,
   dynamicProperty = (vmodl.DynamicProperty) [],
   usbHidCode = 327687,
   modifiers = <unset>
}
(vim.vm.UsbScanCodeSpec.KeyEvent) {
   dynamicType = <unset>,
   dynamicProperty = (vmodl.DynamicProperty) [],
   usbHidCode = 393223,
   modifiers = (vim.vm.UsbScanCodeSpec.ModifierType) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      leftControl = <unset>,
      leftShift = true,
      leftAlt = <unset>,
      leftGui = <unset>,
      rightControl = <unset>,
      rightShift = <unset>,
      rightAlt = <unset>,
      rightGui = <unset>
   }
}
(vim.vm.UsbScanCodeSpec.KeyEvent) {
   dynamicType = <unset>,
   dynamicProperty = (vmodl.DynamicProperty) [],
   usbHidCode = 458759,
   modifiers = (vim.vm.UsbScanCodeSpec.ModifierType) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      leftControl = true,
      leftShift = <unset>,
      leftAlt = <unset>,
      leftGui = <unset>,
      rightControl = <unset>,
      rightShift = <unset>,
      rightAlt = <unset>,
      rightGui = <unset>
   }
}
```
