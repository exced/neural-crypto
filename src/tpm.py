import numpy as np
import hashlib

def theta(t1, t2):
    return 1 if t1 == t2 else 0

class TPM:
    '''TPM
    Tree Parity Machine is a special type of multi-layer feed-forward neural network.
    K - number of hidden neurons
    N - number of input neurons connected to each hidden neuron
    L - range of each weight ({-L,..,0,..,+L })
    W - weight matrix between input and hidden layers. Dimensions : [K, N]
    tau - output score
    '''
    def __init__(self, K=8, N=12, L=4):
        self.K = K
        self.N = N
        self.L = L
        self.W = np.random.randint(-L, L + 1, [K, N])
        self.tau = 0

    def get_output(self, X):
        '''
        Returns a binary digit tau for a given random vecor.
        X - Input random vector
        '''
        X = X.reshape([self.K, self.N])

        sigma = np.sign(np.sum(X * self.W, axis=1))
        tau = np.prod(sigma)

        self.X = X
        self.sigma = sigma
        self.tau = tau

        return tau

    def hebbian(self, tau1, tau2):
        '''
        hebbian update rule
        '''
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] += self.X[i, j] * tau1 * theta(self.sigma[i], tau1) * theta(tau1, tau2)
            self.W[i, j] = np.clip(self.W[i, j] , -self.L, self.L)

    def anti_hebbian(self, tau1, tau2):
        '''
        anti-hebbian update rule
        '''
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] -= self.X[i, j] * tau1 * theta(self.sigma[i], tau1) * theta(tau1, tau2)
            self.W[i, j] = np.clip(self.W[i, j], -self.L, self.L)

    def random_walk(self, tau1, tau2):
        '''
        random walk update rule
        '''
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] += self.X[i, j] * theta(self.sigma[i], tau1) * theta(tau1, tau2)
            self.W[i, j] = np.clip(self.W[i, j] , -self.L, self.L)        

    def update(self, tau2, update_rule='hebbian'):
        '''
        Updates the weights according to the specified update rule.
        tau2 - Output bit from the other machine;
        update_rule - The update rule : ['hebbian', 'anti_hebbian', random_walk']
        '''
        if self.tau == tau2:
            if update_rule == 'hebbian':
                self.hebbian(self.tau, tau2)
            elif update_rule == 'anti_hebbian':
                self.anti_hebbian(self.tau, tau2)
            elif update_rule == 'random_walk':
                self.random_walk(self.tau, tau2)
            else:
                raise Exception("Invalid update rule. Valid update rules are: " + 
                    "\'hebbian\', \'anti_hebbian\' and \'random_walk\'.")

    #make key from weight matrix
    def makeKey(self, key_length):
        '''makeKey
        weight matrix to key and iv : use sha256 on concatenated weights 
        '''
        key = ''
        iv = ''
        # generate key
        for (i, j), _ in np.ndenumerate(self.W):
            if i == j:
                iv += str(self.W[i, j])
            key += str(self.W[i, j])
        # sha1 iv
        hash_object_iv = hashlib.sha1(iv)
        hex_dig_iv = hash_object_iv.hexdigest()            
        # sha256 key
        hash_object_key = hashlib.sha256(key)
        hex_dig_key = hash_object_key.hexdigest()
        return (hex_dig_key[0:int(key_length / 4)], hex_dig_iv)

