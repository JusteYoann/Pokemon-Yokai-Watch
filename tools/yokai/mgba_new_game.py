"""Start a real new game with controller input; return initialized field emulator."""
from mgba_rpc import Emulator


def new_game(gender=0, nuzlocke=False, difficulty_capture=None):
    r=Emulator();rev={v|1:k for k,v in r.symbols.items()}
    def tasks():
        return {rev.get(r.u32(r.symbols['gTasks']+40*i),'?') for i in range(16)
                if r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01'}
    def pulse(key,after=8):
        r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(after)
    def wait(task,press=True):
        for f in range(15000):
            r.keys={8} if press and f%16<4 else set();r.run()
            if task in tasks():r.keys=set();return
        raise AssertionError(('New-game task not reached',task,tasks()))
    try:
        wait('Task_OakSpeech_HandleGenderInput')
        if gender:pulse(5,4)
        pulse(8,0)
        if 'Task_HandleDifficulty' in r.symbols:
            wait('Task_HandleDifficulty')
            if difficulty_capture:
                r.frame.save(difficulty_capture)
            if nuzlocke:pulse(5,4)
            pulse(8,0)
        wait('Task_OakSpeech_YourNameWhatIsIt',False);r.run(60)
        for f in range(8000):
            r.keys={8} if f%16<4 else set();r.run()
            if 'Naming' in rev.get(r.u32(r.symbols['gMain']+4),''):break
        else:raise AssertionError('Player naming not reached')
        r.keys=set();r.run(180)
        pulse(8,15);pulse(8,15);pulse(3,15);pulse(8,20)
        wait('Task_OakSpeech_HandleConfirmNameInput');r.keys=set();r.run(180);pulse(8,0)
        for f in range(15000):
            r.keys={8} if f%16<4 else set();r.run()
            if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
        else:raise AssertionError('New game never reached initial room')
        r.keys=set();r.run(180)
        assert r.u32(r.symbols['gSoundInfo'])==0x68736D53
        return r
    except BaseException:
        r.close();raise
