import rtmidi

def list_midi_ports():
    midiout = rtmidi.RtMidiOut()
    available_ports = []

    for i in range(midiout.getPortCount()):
        port_name = midiout.getPortName(i)
        available_ports.append(port_name)

    print("Available MIDI Ports:")
    for i, port_name in enumerate(available_ports, 1):
        print(f"{i}. {port_name}")

if __name__ == "__main__":
    list_midi_ports()
