import backend
import argparse

parser = argparse.ArgumentParser("Run the server with arguments.")
parser.add_argument("--host", action="store",
                    help="host IP address on which the app runs. Default value is 127.0.0.1.")
parser.add_argument("--port", action="store",
                    help="port number on which the app runs. Default value is 5000.")

args = parser.parse_args()

# Run in console
# python3 EmotionaYouTube --host --port
if args.host and args.port:
    backend.app.app.run(host=args.host, port=args.port)
elif args.host:
    backend.app.app.run(host=args.host, port=5000)
elif args.port:
    backend.app.app.run(host="127.0.0.1", port=args.port)
else:
    backend.app.app.run(host="127.0.0.1", port=5000)
