import numpy as np
import time
import tensorflow as tf
from tensorflow import keras
from keras import layers
from Environment import *
from Parameters import *
from Model import *
from Disable_Print import *

# Disable Printing So we avoid the 1/1 [=======.. output
blockPrint()
initial_time = time.time()

# Configuration paramaters for the whole setup

gamma = 0.99  # Discount factor for past rewards
epsilon = 1.0  # Epsilon greedy parameter
epsilon_min = 0.1  # Minimum epsilon greedy parameter
epsilon_max = 1.0  # Maximum epsilon greedy parameter
epsilon_interval = (
    epsilon_max - epsilon_min
)  # Rate at which to reduce chance of random action being taken
batch_size = 32  # Size of batch taken from replay buffer
max_steps_per_episode = 10000

# Warp the frames, grey scale, stake four frame and scale to smaller ratio
env = create_environment()

# The first model makes the predictions for Q-values which are used to
# make a action.
if default_model == "":
    model = create_q_model()
else:
    model = load_model()

# Build a target model for the prediction of future rewards.
# The weights of a target model get updated every 10000 steps thus when the
# loss between the Q-values is calculated the target Q-value is stable.
model_target = create_q_model()

# In the Deepmind paper they use RMSProp however then Adam optimizer
# improves training time
optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)

# Experience replay buffers
action_history = []
state_history = []
state_next_history = []
rewards_history = []
done_history = []
episode_reward_history = []
running_reward = 0
episode_count = 0
frame_count = 0
# Number of frames to take random action and observe output
epsilon_random_frames = 50000
# Number of frames for exploration
epsilon_greedy_frames = 1000000.0
# Maximum replay length
# Note: The Deepmind paper suggests 1000000 however this causes memory issues
max_memory_length = 100000
# Train the model after each action
update_after_actions = 1
# How often to update the target network
update_target_network = 10000
# Using huber loss for stability
loss_function = keras.losses.Huber()

while True:  # Run until solved
    state = env.reset()
    episode_reward = 0 
    for timestep in range(1, max_steps_per_episode):
        # env.render(); Adding this line would show the attempts
        # of the agent in a pop up window.
        frame_count += 1

        # Use epsilon-greedy for exploration
        if frame_count < epsilon_random_frames or epsilon > np.random.rand(1)[0]:
            # Take random action
            random_action = np.random.choice(env.get_action_space())
            possible_actions = env.get_action_space()

            action = possible_actions.index(random_action)
        else:
            # Predict action Q-values
            # From environment state
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)

            action_probs = model(state_tensor, training=False)[0]
            possible_actions = env.get_action_space()
            action_probs = env.clip_action_probs(possible_actions,action_probs)
            # Take best action
            action = np.argmax(action_probs)

            # reset possible actions so that the indices match up
            possible_actions = ['w','a','s','d'] 

        # Decay probability of taking random action
        epsilon -= epsilon_interval / epsilon_greedy_frames
        epsilon = max(epsilon, epsilon_min)

        # Apply the sampled action in our environment
        try:
            state_next, reward, done = env.step(action) 
        except:
            enablePrint()
            print(action)
            print(action_probs)
            print(possible_actions)
            blockPrint()

        episode_reward += reward

        # Save actions and states in replay buffer
        action_history.append(action)
        state_history.append(state)
        state_next_history.append(state_next)
        done_history.append(done)
        rewards_history.append(reward)
        state = state_next

        # Update every fourth frame and once batch size is over 32
        if frame_count % update_after_actions == 0 and len(done_history) > batch_size:

            # Get indices of samples for replay buffers
            indices = np.random.choice(range(len(done_history)), size=batch_size)
            

            # Using list comprehension to sample from replay buffer
            state_sample = np.array([state_history[i] for i in indices],copy=True)
            state_next_sample = np.asarray([state_next_history[i] for i in indices])
            rewards_sample = [rewards_history[i] for i in indices]
            action_sample = [action_history[i] for i in indices]
            done_sample = tf.convert_to_tensor(
                [float(done_history[i]) for i in indices]
            )

            # Build the updated Q-values for the sampled future states
            future_rewards = model_target.predict(state_next_sample,batch_size=batch_size)

            # Q value = reward + discount factor * expected future reward
            # print(rewards_sample)
            # print(np.shape(future_rewards))
            updated_q_values = rewards_sample + gamma * tf.reduce_max(
                future_rewards, axis=1
            )

            # If final frame set the last value to -1
            updated_q_values = updated_q_values * (1 - done_sample) - done_sample

            # Create a mask so we only calculate loss on the updated Q-values
            masks = tf.one_hot(action_sample, 4)
            # print("action_sample")

            with tf.GradientTape() as tape:
                # Train the model on the states and updated Q-values
                q_values = model(state_sample)
               
                # print("q_values",q_values[0],"\n","masks",masks.shape)
                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                # Calculate loss between new Q-value and old Q-value
                loss = loss_function(updated_q_values, q_action)

            # Backpropagation
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if frame_count % update_target_network == 0:
            # update the the target network with new weights
            model_target.set_weights(model.get_weights())
            weights = np.array(model.get_weights())
            # np.savetxt('data.csv', weights, delimiter=',')
            # Log details
            template = "running reward: {:.2f} at episode {}, frame count {}, time {}"
            enablePrint()
            print(template.format(running_reward, episode_count, frame_count, (time.time()-initial_time)//60))
            blockPrint()

        # Limit the state and reward history
        if len(rewards_history) > max_memory_length:
            del rewards_history[:1]
            del state_history[:1]
            del state_next_history[:1]
            del action_history[:1]
            del done_history[:1]

        # extra output for more visuals
        # if frame_count % 1000 == 0:
        #     enablePrint()
        #     print("Frame= {}".format(frame_count))
        #     blockPrint()

        if done:
            break

    # Update running reward to check condition for solving
    episode_reward_history.append(episode_reward)
    if len(episode_reward_history) > 100:
        del episode_reward_history[:1]
    running_reward = np.mean(episode_reward_history)

    episode_count += 1

    if running_reward > 20000:  # Condition to consider the task solved
        enablePrint()
        print("Solved at episode {}!".format(episode_count))
        blockPrint()
        break

save_model(model)
