import simpy

env = simpy.Environment()

#simulation-sequence
def process(env, resource)
req = resource.request()
yield resource.request()
print(f"resource acquired at {env.now}")

yield env.timeout(5)
print(f"process using resource at {env.now}")

resource.release(req)
print(f"resource released at {env.now}")

#definitions
resource = simpy.Resource(env,capacity=1)
env.process(process(env,resource))

#start of simulation
env.run(until=10)
