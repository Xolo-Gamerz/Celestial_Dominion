#!/usr/bin/env python3
"""Send an ICCCM WM_DELETE_WINDOW request directly to an X11 client."""
import ctypes
import ctypes.util
import sys


class XClientMessageData(ctypes.Union):
    _fields_ = [
        ("b", ctypes.c_char * 20),
        ("s", ctypes.c_short * 10),
        ("l", ctypes.c_long * 5),
    ]


class XClientMessageEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
        ("message_type", ctypes.c_ulong),
        ("format", ctypes.c_int),
        ("data", XClientMessageData),
    ]


class XEvent(ctypes.Union):
    _fields_ = [
        ("type", ctypes.c_int),
        ("xclient", XClientMessageEvent),
        ("pad", ctypes.c_long * 24),
    ]


def main():
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} WINDOW_ID")

    window = int(sys.argv[1], 0)
    library = ctypes.util.find_library("X11")
    if not library:
        raise SystemExit("libX11 could not be located")
    x11 = ctypes.CDLL(library)

    x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x11.XOpenDisplay.restype = ctypes.c_void_p
    x11.XCloseDisplay.argtypes = [ctypes.c_void_p]
    x11.XInternAtom.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
    x11.XInternAtom.restype = ctypes.c_ulong
    x11.XGetWMProtocols.argtypes = [
        ctypes.c_void_p, ctypes.c_ulong,
        ctypes.POINTER(ctypes.POINTER(ctypes.c_ulong)),
        ctypes.POINTER(ctypes.c_int),
    ]
    x11.XGetWMProtocols.restype = ctypes.c_int
    x11.XFree.argtypes = [ctypes.c_void_p]
    x11.XSendEvent.argtypes = [
        ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int,
        ctypes.c_long, ctypes.POINTER(XEvent),
    ]
    x11.XSendEvent.restype = ctypes.c_int
    x11.XSync.argtypes = [ctypes.c_void_p, ctypes.c_int]

    display = x11.XOpenDisplay(None)
    if not display:
        raise SystemExit("Could not connect to the X11 display")

    try:
        protocols_atom = x11.XInternAtom(display, b"WM_PROTOCOLS", 0)
        delete_atom = x11.XInternAtom(display, b"WM_DELETE_WINDOW", 0)
        protocols = ctypes.POINTER(ctypes.c_ulong)()
        count = ctypes.c_int()
        if not x11.XGetWMProtocols(
            display, window, ctypes.byref(protocols), ctypes.byref(count)
        ):
            raise SystemExit(f"Could not read WM_PROTOCOLS for X11 window {window}")
        try:
            if not any(protocols[i] == delete_atom for i in range(count.value)):
                raise SystemExit(
                    f"X11 window {window} does not advertise WM_DELETE_WINDOW"
                )
        finally:
            if protocols:
                x11.XFree(protocols)

        event = XEvent()
        event.xclient.type = 33  # ClientMessage
        event.xclient.send_event = 1
        event.xclient.display = display
        event.xclient.window = window
        event.xclient.message_type = protocols_atom
        event.xclient.format = 32
        event.xclient.data.l[0] = delete_atom
        event.xclient.data.l[1] = 0  # CurrentTime
        if not x11.XSendEvent(display, window, 0, 0, ctypes.byref(event)):
            raise SystemExit(f"XSendEvent failed for X11 window {window}")
        x11.XSync(display, 0)
    finally:
        x11.XCloseDisplay(display)


if __name__ == "__main__":
    main()
