Transmit keystrokes to a running vSphere virtual machine via [pyvmomi](https://github.com/vmware/pyvmomi).

Can be used either as a command-line tool directly, or import as a module.


## Usage
```
usage: send-keys-to-vm [--file in.txt] [--characters 'a long line of text'] [--raw-scancode I]
                       [--modifier {shift,alt,meta,ctrl}] [--moref MOREF] [--uuid UUID] [--ip IP] [-v] [--whatif]
                       [--insecure] [--hostname vCenter Server or ESXi host] [--port vCenter Server Port]
                       [--username USERNAME] [--password PASSWORD]
                       [keys ...]
```

## Examples

Pass characters as a quoted string.

```sh
send-keys-to-vm --characters "sudo tailscale up --auth-key=tskey-auth-1234567890 --ssh"
```

Restart, and trigger a network boot.

```sh
send-keys-to-vm ctrl+alt+delete
sleep 1
send-keys-to-vm F12
```

Open a config file for appending, then stream in some text.

```sh
echo "cat >> .ssh/authorized_keys" | send-keys-to-vm --moref 24
cat ~/.ssh/id_rsa.pub | send-keys-to-vm --moref 24 --file -
.venv/bin/send-keys-to-vm --moref 24 ctrl+d
```

Dump raw KeyEvent list.

```sh
send-keys-to-vm a b C ctrl+d --whatif

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
