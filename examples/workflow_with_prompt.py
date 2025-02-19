from stockwhisper.workflow import SqlWhisperWorkflow
from stockwhisper.actors import stock_actor, toy_actor, artist_actor
import argparse
import asyncio

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run SqlWhisperWorkflow with different actors')
    parser.add_argument('-d', '--domain', choices=['stock', 'toy', 'artist'], 
                        default='stock', help='Domain actor to use (default: stock)')
    
    args = parser.parse_args()
    
    # Select actor based on argument
    actors = {
        'stock': stock_actor,
        'toy': toy_actor,
        'artist': artist_actor
    }
    
    selected_actor = actors.get(args.domain, stock_actor)
    
    query_str = input("Enter query: ")
    w = SqlWhisperWorkflow(selected_actor)
    result = await w.run(query_str=query_str)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
