#DO NOT DELETE THESE LINES
import cards, random
random.seed(100) # random number generator will always generate
                 # the same 'random' number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from end of Tableau pile s to end of pile d.
    MTF s d: Move card from end of Tableau pile s to Foundation d.
    U: Undo the last valid move.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''

  
def fix_kings(tableau):
    ''' Go through each of the lists of lists and make sure that for any kings in the deck
     there is nothing to its left other than another king '''
    for i in tableau:
        if len(i) == 3:
            for j in range(5): # this runs it 5 times (min is 3 ik but idc) so it sorts all the cards and 2x to double check
                if i[1].rank() == 13 and i[0].rank() != 13: # if second card = king but not first
                    temp = i[0]
                    i[0] = i[1]
                    i[1] = temp
                elif i[2].rank() == 13 and i[1].rank() != 13: # if the third card = king but not second
                    temp = i[1]
                    i[1] = i[2]
                    i[2] = temp

    return tableau

                
def initialize():
    ''' Create the foundation and the tableau '''
    foundation = [[], [], [], []]
    tableau = []
    deck = cards.Deck()
    deck.shuffle()
    for i in range(18):
        stack = []
        for j in range(3):
            if deck.is_empty() == False:
                stack.append(deck.deal())
            else:
                break
        tableau.append(stack)
    tableau = fix_kings(tableau)
    return (tableau, foundation)


def get_option():
    ''' Prompts user for an option and then returns what they gave '''

    while True:
        b = input("\nInput an option (MTT,MTF,U,R,H,Q): ")
        option = b.upper()
        if option[0:3] != "MTT" and option[0:3] != "MTF" and option != "U" and option != "R" and option != "H" and\
                option != "Q":
            print("Error in option:", b)
            return None
        else:
            a = option.split()
            if a[0].lower() == "mtf":
                if int(a[1]) > 17 or int(a[1]) < 0:
                    print("Error in Source.")
                    return None
                if int(a[2]) > 5 or int(a[2]) < 0:
                    print("Error in Destination.")
                    return None
            if a[0].lower() == "mtt":
                if int(a[1]) > 17 or int(a[1]) < 0:
                    print("Error in Source.")
                    return None
                if int(a[2]) > 17 or int(a[2]) < 0:
                    print("Error in Destination.")
                    return None
            if len(a) > 2:
                return [a[0].upper(), int(a[1]), int(a[2])]
            else:
                return [a[0].upper()]

          
def valid_tableau_to_tableau(tableau,s,d):
    ''' Validate whether the move from t to t is valid and return a bool '''
    if len(tableau[d]) == 3 or len(tableau[d]) == 0:
        return False
    elif len(tableau[s]) == 0:
        return False
    elif tableau[d][-1].rank() + 1 == tableau[s][-1].rank() or tableau[d][-1].rank() - 1 == tableau[s][-1].rank():
        return True


def valid_tableau_to_foundation(tableau,foundation,s,d):
    ''' Validate whether the move from t to v is valid and return a bool '''
    if len(tableau[s]) > 0:
        if len(foundation[d]) == 0 and tableau[s][-1].rank() == 1:
            return True
        if len(foundation[d]) > 0 :
            if foundation[d][-1].suit() == tableau[s][-1].suit() and (foundation[d][-1].rank() + 1 == tableau[s][-1].rank() or foundation[d][-1].rank() - 1 == tableau[s][-1].rank()):
                return True
    return False


def move_tableau_to_tableau(tableau,s,d):
    ''' Move the respective card to where it should go '''
    if valid_tableau_to_tableau(tableau,s,d):
        tableau[d].append(tableau[s][-1])
        tableau[s].pop(-1)
        return True
    else:
        return False


def move_tableau_to_foundation(tableau, foundation, s,d):
    ''' Move the respective card to where it should go '''
    if valid_tableau_to_foundation(tableau, foundation, s, d):
        foundation[d].append(tableau[s][-1])
        tableau[s].pop(-1)
        return True
    else:
        return False


def check_for_win(foundation):
    ''' checks to make sure that all of the foundations are full '''
    n = 0
    for i in foundation:
        if len(i) == 13:
            n += 1
    if n == 4:
        return True
    else:
        return False


def undo(moves,tableau,foundation):
    '''
    Undo the last move;
       Parameters:
           moves: the history of all valid moves. It is a list of tuples 
                  (option,source,dest) for each valid move performed since the 
                  start of the game. 
           tableau: the data structure representing the tableau.  
       Returns: Bool (True if there are moves to undo. False if not)
    '''
       
    if moves: # there exist moves to undo
        last_move = moves.pop()
        option = last_move[0]
        source = last_move[1]
        dest = last_move[2]
        print("Undo:",option,source,dest)
        if option == 'MTT':
            tableau[source].append(tableau[dest].pop())
        else: # option == 'MTF'
            tableau[source].append(foundation[dest].pop())
        return True
    else:
        return False


def display(tableau, foundation):
    '''Display the foundation in one row;
       Display the tableau in 3 rows of 5 followed by one row of 3.
       Each tableau item is a 3-card pile separated with a vertical bar.'''
    print("\nFoundation:")
    print(" "*15,end='') # shift foundation toward center
    # display foundation with labels
    for i,L in enumerate(foundation):
        if len(L)==0:
            print("{:d}:    ".format(i),end="  ") # padding for empty foundation slot
        else:
            print("{:d}: {} ".format(i,L[-1]),end="  ") # display only "top" card
    print()
    print("="*80)
    print("Tableau:")
    # First fifteen 3-card piles are printed; across 3 rows
    for i in range(15):
        print("{:2d}:".format(i),end='') # label each 3-card pile
        for c in tableau[i]:  # print 3-card pile (list)
            print(c,end=" ")
        print("    "*(3-len(tableau[i])),end='') # pad with spaces
        print("|",end="")
        if i%5 == 4: # start a new line after printing five lists
            print()
            print("-"*80)
    # Final row of only three 3-card piles is printed
    print(" "*15+"|",end='')  # shift first pile right
    for i in range(15,18):
        print("{:2d}:".format(i),end='') # label each 3-card pile
        for c in tableau[i]:
            print(c,end=" ")
        print("    "*(3-len(tableau[i])),end='') # pad with spaces
        print("|",end="")
    print()
    print("-"*80)
    

def main():  
    ''' This is the function where all the other functions get called so that the game works '''
    game = initialize()
    foundation = game[1]
    tableau = game[0]
    print("\nWelcome to Shamrocks Solitaire.\n")
    display(tableau, foundation)
    print(MENU)
    option = get_option()
    while option == None:
        option = get_option()
    a = option[0].upper()
    move = []
    while a != "Q":
        if a == "MTT":
            if move_tableau_to_tableau(tableau, int(option[1]), int(option[2])):
                t = (option[0], option[1], option[2])
                move.append(t)
                if check_for_win(foundation) == False:
                    display(tableau, foundation)
            else:
                print("Error in move: {} , {} , {}".format(a,int(option[1]), int(option[2])))

        elif a == "MTF":
            if move_tableau_to_foundation(tableau, foundation, int(option[1]), int(option[2])):
                t = (option[0], option[1], option[2])
                move.append(t)
                if check_for_win(foundation) == False:
                    display(tableau, foundation)
            else:
                print("Error in move: {} , {} , {}".format(a, int(option[1]), int(option[2])))

        elif a == "U":
            if undo(move, tableau, foundation):
                # print("Undo: {} , {} , {}".format(move[-1][0], move[-1][1], move[-1][2]))
                display(tableau, foundation)
            else:
                print("No moves to undo.")

        elif a == "R":
            print("\n- - - - New Game. - - - -")
            game = initialize()
            foundation = game[1]
            tableau = game[0]
            print("\nWelcome to Shamrocks Solitaire.\n")
            display(tableau, foundation)
            print(MENU)

        elif a == "H":
            print(MENU)

        if check_for_win(foundation):
            print("You won!")
            display(tableau, foundation)
            print("\n- - - - New Game. - - - -")
            game = initialize()
            foundation = game[1]
            tableau = game[0]
            display(tableau, foundation)
            print(MENU)

        option = get_option()
        while option == None:
            option = get_option()
        a = option[0].upper()

    print("Thank you for playing.")


if __name__ == '__main__':
     main()
