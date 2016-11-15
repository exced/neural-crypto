from tpm import TPM
import numpy as np
import time, sys, getopt
import matplotlib.pyplot as plt

def random(K, N, L):
    '''random
    return a random vector input for TPM
    '''
    return np.random.randint(-L, L + 1, [K, N])

def sync_score(TPM1, TPM2, L):
    '''sync_score
    Synchronize the score of 2 tree parity machines
    TPM1 - Tree Parity Machine 1
    TPM2 - Tree Parity Machine 2
    '''
    return 1.0 - np.average(1.0 * np.abs(TPM1.W - TPM2.W)/(2 * L))

def main(argv):
    # default Tree Parity Machine parameters
    K = 8
    N = 12
    L = 4
    key_length = 128 #bits
    iv_length = 128 #bits
    update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
    update_rule = update_rules[0]
    input_file = ''
    output_file = 'out.enc'
    has_input_file = False
    try:
        opts, args = getopt.getopt(argv,"hK:N:L:k:v:i:o:",["K=","N=","L=","k=","v=","i=","o="])
    except getopt.GetoptError:
        print 'unknown options'
        print 'run.py -i <input file> -o <output file> -K <nb hidden neurons> -N <nb input neurons> -L <range of weight> -k <key length> -v <iv length>'
        print 'key length options : 128, 192, 256'
        print 'iv length : [0:256] multiple of 4'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'run.py -i <input file> -o <output file> -K <nb hidden neurons> -N <nb input neurons> -L <range of weight> -k <key length> -v <iv length>'
            print 'default values : K=8, N=12, L=4'
            print 'key length options : 128, 192, 256'
            print 'iv length : [0:256]'
            sys.exit()
        elif opt in ("-i", "--i"):
            has_input_file = True
            input_file = arg
        elif opt in ("-o", "--o"):
            output_file = int(arg)
        elif opt in ("-K", "--K"):
            K = int(arg)
        elif opt in ("-N", "--N"):
            N = int(arg)
        elif opt in ("-L", "--L"):
            L = int(arg)
        elif opt in ("-v", "--v"):
            iv_length = int(arg)            
        elif opt in ("-k", "--k"):
            if arg == "128" or arg == "192" or arg == "256":
                key_length = int(arg) 
            else:
                print 'non available key options'
                print 'key length options : 128, 192, 256'
                sys.exit()

    #Create TPM for Alice, Bob and Eve. Eve eavesdrops communication of Alice and Bob
    print "Creating machines : K=" + str(K) + ", N=" + str(N) + ", L=" + str(L) + ", k=" + str(key_length) + ", v=" + str(iv_length)
    Alice = TPM(K, N, L)
    Bob = TPM(K, N, L)
    Eve = TPM(K, N, L)

    #Synchronize weights
    nb_updates = 0 
    nb_eve_updates = 0 
    start_time = time.time() # Start time
    sync_history = [] # plot purpose
    sync_history_eve = [] # plot purpose
    score = 0 # synchronisation score of Alice and Bob 

    while score < 100:

        X = random(K, N, L) # Create random vector [K, N]

        # compute outputs of TPMs
        tauA = Alice.get_output(X) 
        tauB = Bob.get_output(X) 
        tauE = Eve.get_output(X)

        Alice.update(tauB, update_rule) 
        Bob.update(tauA, update_rule) 

        #Eve would update only if tauA = tauB = tauE
        if tauA == tauB == tauE:
            Eve.update(tauA, update_rule)
            nb_eve_updates += 1

        nb_updates += 1
        # sync of Alice and Bob
        score = 100 * sync_score(Alice, Bob, L) # Calculate the synchronization of Alice and Bob
        sync_history.append(score) # plot purpose
        # sync of Alice and Eve
        score_eve = 100 * sync_score(Alice, Eve, L) # Calculate the synchronization of Alice and Eve
        sync_history_eve.append(score_eve) # plot purpose        

        sys.stdout.write("\r" + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(nb_updates) + " / Eve's updates = " + str(nb_eve_updates)) 

    end_time = time.time()
    time_taken = end_time - start_time 

    # results
    print "\nTime taken = " + str(time_taken)+ " seconds."
    Alice_key, Alice_iv = Alice.makeKey(key_length, iv_length)
    Bob_key, Bob_iv = Bob.makeKey(key_length, iv_length)
    Eve_key, Eve_iv = Eve.makeKey(key_length, iv_length)
    print "Alice's gen key = " + str(len(Alice_key)) + " key : " + Alice_key + " iv : " + Alice_iv;
    print "Bob's gen key = " + str(len(Bob_key)) + " key : " + Bob_key + " iv : " + Bob_iv;
    print "Eve's gen key = " + str(len(Eve_key)) + " key : " + Eve_key + " iv : " + Eve_iv;

    if Alice_key == Bob_key and Alice_iv == Bob_iv:
        if has_input_file:
            import subprocess
            # cipher with Alice key and IV
            bashCommand = "openssl enc -aes"+ str(key_length) +" -K "+ Alice_key + " -iv " + Alice_iv +" -in " + input_file +  " -out " + output_file
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            # decipher with Bob key and IV
            bashCommand = "openssl enc -aes"+ str(key_length) +" -K "+ Alice_key + " -iv " + Alice_iv +" -in " + output_file +  " -out " + "decipher.txt" + " -d"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()            
            print "encryption and decryption with aes" + str(key_length) + " done."
    else:
        print "error, Alice and Bob have different key or iv : cipher impossible"            

    #Plot graph 
    plt.figure(1)
    plt.title('Synchronisation')
    plt.ylabel('sync %')
    plt.xlabel('nb iterations')
    sync_AB, = plt.plot(sync_history)
    sync_Eve, = plt.plot(sync_history_eve)
    plt.legend([sync_AB, sync_Eve], ["sync Alice Bob", "sync Alice Eve"])
    plt.show()

if __name__ == "__main__":
   main(sys.argv[1:])


