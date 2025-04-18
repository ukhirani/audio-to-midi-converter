import pyaudio

def list_audio_input_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    print("Available Audio Input Devices:")
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"{i}. {device_info['name']}")

if __name__ == "__main__":
    list_audio_input_devices()
