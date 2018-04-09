
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('x',help="The Fibonacci number "+ "you with to calculate", type=int)
    parser.add_argument('y', help="The Fibonacci number " + "you with to calculate", type=int)
    args=parser.parse_args()
    result=add(args.x,args.y)
    print(result)


def add(x,y):
    return x+y

if __name__=='__main__':
    main()



