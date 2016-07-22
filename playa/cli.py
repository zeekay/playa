import argparse
import json
import os.path
import spotipy
import spotipy.util as util
import sys

def read_token():
    with open(os.path.expanduser('~/.playa')) as f:
        return json.load(f)['token']

def command_token(args):
    token = util.prompt_for_user_token(args.username)
    if token:
        print token
        with open(os.path.expanduser('~/.playa'), 'w') as f:
            f.write(json.dumps({'token': token}))
    else:
        print "Can't get token for", args.username

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %32.32s %s" % (i, track['artists'][0]['name'], track['album']['name'], track['name']))

def command_playlists(args):
    sp = spotipy.Spotify(auth=read_token())

    # Get playlists for given user
    playlists = sp.user_playlists(args.username)

    for playlist in playlists['items']:
        # Skip if not user's playlist
        if playlist['owner']['id'] != args.username:
            continue

        # Print each playlist name
        print playlist['name']

        # Get tracks for given playlist
        results = sp.user_playlist(args.username, playlist['id'], fields="tracks,next")
        tracks = results['tracks']

        # print Tracks
        show_tracks(tracks)
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    token_parser = subparsers.add_parser('token', help='authenticate and save access token')
    token_parser.set_defaults(command=command_token)
    token_parser.add_argument('username', help='username')

    playlists_parser = subparsers.add_parser('playlists', help='list playlists for a user')
    playlists_parser.set_defaults(command=command_playlists)
    playlists_parser.add_argument('username', help='username')

    args = parser.parse_args()

    try:
        cmd = args.command
    except AttributeError:
        parser.print_help()
        return
    try:
        cmd(args)
    except KeyboardInterrupt:
        print('')
        sys.exit(1)
