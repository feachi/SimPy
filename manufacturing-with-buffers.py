import simpy
import random
RANDOM_SEED = 42
SIM_TIME = 1000
# zeit
TIME_SCHWEISSEN = 5
TIME_LACKIEREN = 8
TIME_QS = 3
# buf
buf1 = simpy.Container(env, init=0, capacity=CAP_BUF1)
CAP_BUF1 = 10
buf2 = simpy.Container(env, init=0, capacity=CAP_BUF2)
CAP_BUF2 = 10
buf3 = simpy.Container(env, init=0, capacity=CAP_BUF3)
CAP_BUF3 = 10

#prozess: quelle -> puffer -> schweißen -> puffer -> lackieren -> puffer -> QS -> drain
def part_process(env, name, buf1, res_schweißen, buf2, res_lackieren, buf3, res_qs):
    """The lifecycle of a single part through the system."""
    # enter buf1
    yield buf1.put(1)
    with res_schweißen.request() as req:
        yield req
        yield buf1.get(1)
        yield env.timeout(random.expovariate(1.0 / TIME_SCHWEISSEN))
    
# enter buf2
    yield buf2.put(1)
    with res_lackieren.request() as req:
        yield req
        yield buf2.get(1)
        yield env.timeout(random.expovariate(1.0 / TIME_LACKIEREN))
        
    #enter buf3
    yield buf3.put(1)
    with res_qs.request() as req:
        yield req
        yield buf3.get(1)
        yield env.timeout(random.expovariate(1.0 / TIME_QS))
    
    print(f"Part {name} finished at {env.now:.2f}")

def source(env, buf1, res_schweißen, buf2, res_lackieren, buf3, res_qs):
    """Generates new parts."""
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / 4)) #quelle
        i += 1
        env.process(part_process(env, f"P{i}", buf1, res_schweißen, buf2, 
                                 res_lackieren, buf3, res_qs))

# drain
# working on it

random.seed(RANDOM_SEED)
env = simpy.Environment()

#resources
res_schweißen = simpy.Resource(env, capacity=1)
res_lackieren = simpy.Resource(env, capacity=1)
res_qs = simpy.Resource(env, capacity=1)

#start
env.process(source(env, buf1, res_schweißen, buf2, res_lackieren, buf3, res_qs))
env.run(until=SIM_TIME)