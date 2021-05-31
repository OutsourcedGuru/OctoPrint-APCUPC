# APCUPC

An OctoPrint plugin for Raspbian to communicate with an APC UPC via serial.

![apc](https://user-images.githubusercontent.com/15971213/54496388-f9427380-48ab-11e9-8049-0ce750b226d1.jpg)

## Overview
> **Raspberry Pi 3B**: A single-board computer made by the Raspberry Pi Foundation
> 
> **UPS**: (abbreviation of Uninterruptible Power Supply) is a battery-based device for providing clean power to personal computers and their peripheral devices.
>
> **apcupsd**: The underlying daemon which communicates to the APC-branded UPS.

* An uninterruptible power supply (UPS) is a great addition to your 3D printer's setup. It can save your print job during momentary loss of power (brownouts) so that it continues without interruption or loss.
* My favorite brand of UPS products is APC and their Back- and Smart-UPS line include a serial connection and cable suitable for communicating with a host computer like the Raspberry Pi in this case. This plugin relies upon that connectivity.
* During an outage longer than a brownout, the plugin will be notified and proceed to 1) pause the print job, 2) cancel the print job and finally, 3) gracefully shutdown your Raspberry Pi. For this reason, your **OctoPrint** -> **Settings** -> **GCode Scripts** -> **After print job is paused** should include gcode to move the hotend to be above your part.
* The installation instructions throughout assume that you have a Raspbian-based Raspberry Pi computer which will support APC's daemon for monitoring that serial connection. It is only meant to be compatible with the four-core versions of the Raspberry Pi computer with 1GB of RAM installed.

### The rationale for this plugin

Rather than rigging up inline switches, ATX hacks or similar...

    ...I thought that I would provide this plugin as a simpler alternative for shutting down your printer.

## Compatibility
This plugin was created to support only the following platforms:

* Raspberry Pi 400
* Raspberry Pi 4B
* Raspberry Pi 3B
* Raspberry Pi 3B+
* Raspberry Pi 2B

It is NOT intended to support the following:

* Raspberry Pi 3A+
* Raspberry Pi Compute Modules
* Raspberry Pi 1B+
* Raspberry Pi 1A+
* Raspberry Pi Zero W
* Raspberry Pi Zero
* PCs, Macs, generic Linux workstations *or anything else*

Also, this plugin is NOT intended to support those of you who wish to plug more than one printer into your Raspberry Pi 3B.

### APC brand

This plugin only supports APC Back-UPS and Smart-UPS devices for which you have the USB-based serial cable.

## Primary use case
I expect that this plugin would be useful for anyone who needs to gracefully shutdown power to their Raspberry Pi during a power outage, minimizing the risk of microSD card corruption.

## Complications

### If other computers are also plugged into your UPS
This plugin can only control the OctoPi-installed Raspberry Pi computer to shut it down in case of power outage. Other computers also plugged into this same UPS would be abruptly powered off.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OutsourcedGuru/OctoPrint-APCUPC/archive/master.zip

For obvious reasons, you need to install APC's USB-based serial cable, connecting one end to a USB Type-A port on your Raspberry Pi and the other end in the pseudo-Ethernet RJ-50 connection. (In some models, this is a USB Type-B connection.)

![RJ50](https://user-images.githubusercontent.com/15971213/54496397-137c5180-48ac-11e9-9e87-a705a48896fe.jpg)

## Configuration

When initially installed, the plugin still needs a script to be run once. The instructions for doing this may be found in the associated **Settings** page.

## Reporting bugs/issues
Please do not report a bug if you find that this doesn't work with a UPS which *isn't* made by APC.

Please do not report a bug if you need support finding your UPS's serial cable; talk to [APC](https://www.apc.com/shop/us/en/categories/power/ups/ups-management/interface-cables/_/N-18ehd8a) about that.

Please do not report a bug if you are plugging more than one printer into your Raspberry Pi 3B at the same time.

Please do not report a bug if you are using a platform that isn't listed in the **Compatibility** section above.
