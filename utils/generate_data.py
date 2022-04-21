import torch

# For Actor-Critic
def generate_a2c_data(num_transitions, gamma, agent, net, env, device):
    games_data = []

    states = []
    actions = []
    rewards = []
    next_states = []

    curr_state = env.reset()
    done = False

    # Statistics
    # num_wins = 0
    # num_losses = 0
    # avg_reward_per_game = 0

    for _ in range(num_transitions):
        pred = agent(torch.Tensor([curr_state['state']], device=device))
        env_action = pred[1][0]
        net_action = pred[0][0]

        next_state, reward, done, _ = env.step(env_action)

        states.append(curr_state['state'])
        actions.append(net_action)
        rewards.append(reward)
        next_states.append(next_state['state'])

        curr_state = next_state

        if done:
            _, bootstrapped_value = net(torch.Tensor([curr_state['state']], device = device))
            bootstrapped_value = bootstrapped_value.detach().squeeze().numpy()

            returns = compute_returns(bootstrapped_value, rewards, gamma)
            game_data = list(zip(states, actions, next_states, returns[::-1]))
            games_data.extend([transition for transition in game_data])

            curr_state = env.reset()
            done = False

            states = []
            actions = []
            rewards = []
            next_states = []

    # Finish off the stragglers
    if(len(states)):
        _, bootstrapped_value = net(torch.Tensor([curr_state['state']], device = device))
        bootstrapped_value = bootstrapped_value.detach().squeeze().numpy()

        returns = compute_returns(bootstrapped_value, rewards, gamma)
        game_data = list(zip(states, actions, next_states, returns[::-1]))

        games_data.extend([transition for transition in game_data])

    assert(len(games_data) == num_transitions)
    return games_data



def compute_returns(bootstrapped_value, rewards, gamma):
    returns = []

    ret = bootstrapped_value
    requires_bootstrap = False
    for reward in rewards[::-1]:
        if requires_bootstrap:
            ret = reward + gamma * ret
            returns.append(ret)
        else:
            returns.append(reward)
        requires_bootstrap = True

    return returns
