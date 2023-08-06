import matplotlib.pyplot as plt
from .preprocessing import load_stock_data
from .RL_algorithms import run_dqn_algorithm, run_ddqn_algorithm, run_dddqn_algorithm

def trade(stock,algorithm):
	data=load_stock_data(stock)
	returns=run_dqn_algorithm(data,algorithm)
	
	plt.plot(range(70), returns, marker='o', linestyle='--', color='g', label='Square') 
	plt.xlabel('Training epochs')
	plt.ylabel('Reward') 
	plt.title('Profit')
	plt.show()
	
