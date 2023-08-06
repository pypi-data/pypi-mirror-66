from enum import Enum
from typing import List
import asyncio
    
class async_state_transition:
    def __init__(self, taskMapName : str, stateToChangeName : str, validEntryStates : List[Enum], transitionState : Enum, signal, *args):
        """
        A decorator for an asyncronous state transition.
        (i,e the state transition request call will return imeditely, but the state transition will only happen in the future).
        After the state transition request call is made, the state will transition to the transitionState, and then will only transition to the
        desired state after an event has occured.
        The request will only be succseffull if the state is currently is one of the validEntryStates, and if it is not currently allready transitioning.
        Requests can be canceled using the cancel() method on the task (See example code).
        The function this is decorating must be a member function, and the owning class must have a dict to store the currenty pending tasks.
        @param taskMapName: The name of the Dict of pending tasks, belonging to the class that owns the member function that this is decorating
        @param stateToChangeName: The name of the state to change, belonging to the class that owns the member function that this is decorating
        @param validEntryStates: a list of enums of possible entry states that this trasition can be made from. If the state to change is not one of these,
            the request will fail
        @param transitionState: if the request is successufull, the state to change will imediely go into this transition state
        @param signal: an awaitable (async) function pointer that blocks the transition from happening imeditely. E.g this could be a timer if the state transition
            should happen afetr a time delay, or it could be a blocking function that waits untill an event has occured.
        @param *args: arguments for the signal. These are optional
        """
        self.__taskMapName = taskMapName
        self.__stateToChangeName = stateToChangeName
        self.__validEntryStates = validEntryStates
        self.__transitionState = transitionState
        self.__signal = signal
        self.__signalArgs = args
        
    def __call__(self, f):
        def wrapped_f(*args):
                        
             # f must be a member function, so arg 0 is self, i.e the class that owns the member function
            obj = args[0]

            # obj must have a task map. the name of the task map is set in __init__
            taskMap = obj.__getattribute__(self.__taskMapName)
            
            # check transition is valid
            if obj.__getattribute__(self.__stateToChangeName) not in self.__validEntryStates:
                print("state \"" + self.__stateToChangeName + "\" can only transition from: " + str(self.__validEntryStates))
                return
            
            if self.__stateToChangeName in taskMap.keys():
                print("state \"" + self.stateToChange + "\" transition already in progress")
                return
            
            obj.__setattr__(self.__stateToChangeName, self.__transitionState) # imeditely transition to the transition state
            
            async def __job():
                await self.__signal(*self.__signalArgs)
                await f(*args) # transition to the final state
                taskMap.pop(self.__stateToChangeName) # remove task from the pending task map

                
            taskMap[self.__stateToChangeName] = asyncio.ensure_future(__job())
                        
        return wrapped_f
 
async def timeDelay(time):
    await asyncio.sleep(time)

#Test
if __name__ == "__main__":
    
    class State(Enum):
        A = 0,
        AB = 1,
        B = 2
    
    class Foo:
        __tasks = {}
        __bar = State.A
        
        @property
        def bar(self): return self.__bar

        @async_state_transition("_Foo__tasks", "_Foo__bar", {State.A}, State.AB, timeDelay, 2)
        async def toB(self):
            self.__bar = State.B
            
        def cancelTransition(self):
            self.__tasks["_Foo__bar"].cancel()
        
    async def main():
        f = Foo()
        print(str(f.bar))
        f.toB()
        print(str(f.bar))
        await asyncio.sleep(3)
        print(str(f.bar))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    
