
import time
import random
import io

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        # these 3 variables are globally used inside the class
        self.t = 0
        self.start = 0
        self.max_depth = 9

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin
            self.path = {}

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again——【！！】very good
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately
    def move(self, a, b, a_fin, b_fin, t):
        #For test only: return a random move
        # r = []
        # for i in range(6):
        #     if a[i] != 0:
        #         r.append(i)
        # # # To test the execution time, use time and file modules
        # # # In your experiments, you can try different depth, for example:
        # # f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # # # Make sure to clean the file before each of your experiment
        # # for d in [3, 5, 7]: #You should try more
        # #     f.write('depth = '+str(d)+'\n')
        # #     t_start = time.time()
        # #     self.minimax(depth = d)
        # #     f.write(str(time.time()-t_start)+'\n')
        # # f.close()
        # return r[random.randint(0, len(r)-1)]
        #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        #and remove timing code.

        #Comment all the code above and start your code here
        state = self.state(a, b, a_fin, b_fin)
        self.t = t
        self.start = time.time()
        # print("=============================")
        value = self.max_value(state, float('-inf'), float('inf'), 0)  # init val for alpha is -inf, init val for beta is inf
        # print("=============================")

        f = open('time_pruning_move_depth9.txt', 'a')
        f.write(str(1000 * (time.time() - self.start)) + 'ms\t' + "limit: "+str(self.t) + 'ms\n')  # 毫秒为单位
        f.close()

        # res is an int
        # choose the biggest value in the path (a dict), and return the key corresponding to that value
        res = max(state.path, key = lambda key: state.path[key])

        return res


    # heuristic (minimax)
    def target_func(self, state):
        """ return the gap between the opponent and me """
        return state.a_fin - state.b_fin

    # terminate based on several conditions:
    # reach max_depth / time consumption exceeds limit / one side's kalah has more than 36 (half of the total) / tie
    def terminal_test(self, state, depth):
        """ stop if the search meets termination """
        return 1000 * (time.time() - self.start) >= self.t or depth >= self.max_depth \
        or state.a_fin > 36 or state.b_fin > 36 or (state.a_fin == state.b_fin == 36)

    
    def run_out_of_stones(self, holes):
        """ return true if no hole contains stones """
        for stones in holes:
            if stones > 0: return False
        return True


    # pass in the original state
    # Attention: action function here is not what happens after we do an actual move. It's just an assumption that we do this move and return a new state
    # The real "action" is implemented in the main.py
    # This action func is a-oriented. We don't need to consider b side since for the opponent he just wants to change a to minimize the target function
    def action(self, hole, state):
        """ return a new state after choosing which hole to move """
        if state.a[hole] == 0: 
            return
        a_new, b_new = state.a[:], state.b[:]  # deep copy
        
        result = self.state(a_new, b_new, state.a_fin, state.b_fin)


        # assign stones to holes counterclockwise
        idx = hole
        n = result.a[hole]
        result.a[hole] = 0
        for i in range(n):
            idx += 1
            if idx == 13:  # go back to the first element in result.a
                idx = 0
                result.a[idx] += 1
            elif idx == 6:
                result.a_fin += 1  # reach kalah
            elif idx > 6 and idx < 13:
                result.b[idx - 7] += 1
            else:
                result.a[idx] += 1


        # If last stone lies in an empty hole, take all the stones in the opponent's opposite hole (if there are stones in that hole)
        if idx < 6 and result.a[idx] == 1:
            oppo = result.b[-(idx+1)]
            if oppo != 0:            
                result.a_fin += oppo
                result.b[-(idx+1)] = 0
                result.a_fin += 1
                result.a[idx] = 0


        # If one side out of stones, then the opponent will move the rest of his stones to his kalah
        if self.run_out_of_stones(result.a):
            for i, stones in enumerate(result.b):
                result.b_fin += stones
                result.b[i] = 0
        
        return result



    def find_successors(self, state):
        """ return successors as (hole, state) tuple """
        successors= {}
        for idx in range(6):
            next = self.action(idx, state)
            if next: successors[idx] = next
        return successors


    # depth means the current depth
    def max_value(self, state, alpha, beta, depth):
        """ return the max heuristic value this state can achieve """
        # print("max_value depth=",depth,"beta=",beta)
        if self.terminal_test(state, depth): 
            # print("reach recursion base, gap=",self.utility(state))
            return self.target_func(state)  # recursion base: gap between a_fin and b_fin
        val = float('-inf')
        for hole, s in self.find_successors(state).items():
            val = max(val, self.min_value(s, alpha, beta, depth + 1))
            state.path[hole] = val  # each state object will have a path dict
            if val >= beta: 
                # print("max_value depth=",depth,"beta=",beta,"cur_hole=",hole)
                # print("v=",v,"so get beta pruning")
                return val  # intelligent strategy: beta pruning, allow stop earlier
            # alpha is the current optimal value based on the visted successors
            alpha = max(alpha, val)
    
        return val

    
    def min_value(self, state, alpha, beta, depth):
        """ return the min heuristic value this state can achieve """
        # print("min_value depth=",depth,"alpha=",alpha)
        if self.terminal_test(state, depth): 
            # print("reach recursion base, gap=",self.utility(state))
            return self.target_func(state) # recursion base: gap between a_fin and b_fin
        val = float('inf')
        for hole, s in self.find_successors(state).items():
            val = min(val, self.max_value(s, alpha, beta, depth + 1))
            if val <= alpha:  # intelligent strategy: alpha pruning, allow stop earlier
                # print("min_value depth=",depth,"alpha=",alpha,"cur_hole=",hole)
                # print("v=",v,"so get alpha pruning")
                return val
            beta = min(beta, val)
        return val

    # calling function
    def minimax(self, depth):
        #example: doing nothing but wait 0.1*depth sec
        time.sleep(0.1*depth)
