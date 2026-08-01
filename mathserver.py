from mcp.server.fastmcp import FastMCP

math=FastMCP("Math")

@math.tool()

def add(a:int,b:int)->int:
    """Add two numbers"""
    return a+b

@math.tool()

def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b


if __name__=="__main__":
    math.run(transport="stdio")
    