import vindinium
import vindinium.bots.states.state_definitions as states

def main():
    # Create a vindinium client
    client = vindinium.Client(
        server='http://aigamesvm:9000',
        key='sui35va8',
        # key='vibet5m0',
        mode='arena', #or training
        n_turns=300,
        open_browser=True
    )

    url = client.run(vindinium.bots.StateMachineBot(states.GoToMineState()))
    print 'Replay in:', url

if __name__ == '__main__':
    main()
