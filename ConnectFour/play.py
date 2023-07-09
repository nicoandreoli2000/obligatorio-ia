from spaceGPT_agent_obf import SpaceGPTAgent

def play_vs_other_agent(env, agent1, agent2, render=True):
    done = False
    obs = env.reset()
    winner = 0
    while not done:
        if render: env.render()
        action = agent1.next_action(obs)
        obs, _, done, _ = env.step(action)

        if render: env.render()
        if not done:
            next_action = agent2.next_action(obs)
            _, _, done, _ = env.step(next_action)

    if render: env.render()
    winner = env._grid.winner
    final_msg = "Player " + str(winner) + " WON!!!" if winner != 0 else "It's a tie!" 
    if render: print(final_msg)
    return final_msg

def play_vs_loaded_agent(env, agent, render=True):
    enemy_agent = load_enemy_agent()
    return play_vs_other_agent(env, agent, enemy_agent, render)

def load_enemy_agent():
    return SpaceGPTAgent(2, 4)
