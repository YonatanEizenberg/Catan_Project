import socket
import pyaudio


class Audio_Client:

    def __init__(self):         # sets the Audio Client
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                self.target_ip = "127.0.0.1"
                self.target_port = 12345

                self.s.connect((self.target_ip, self.target_port))
                print("Audio server connected")
                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024               # size of every packet
        audio_format = pyaudio.paInt16  # format of the audio - 16 bits
        channels = 1                    # number of channels to record/hear from
        rate = 7000                     # rate of the audip

        try:
            # initialise microphone recording
            self.p = pyaudio.PyAudio()
            # setting the playing audio object
            self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                              frames_per_buffer=chunk_size)
            # setting the recording audio object
            self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                                frames_per_buffer=chunk_size)

            print("Connected to Server")
        except:
            print("Audio unavailable")

    def receive_server_data(self):      # the function receives audio from server and play it
        while True:                     # the function is in a Thread and it runs all the time
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):      # the function records audio and sends it to the server
        try:
            data = self.recording_stream.read(1024)
            self.s.sendall(data)
        except:
            pass