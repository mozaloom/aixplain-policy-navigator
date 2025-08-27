import click
import os
from dotenv import load_dotenv
from ..agents.policy_agent import PolicyNavigatorAgent
from ..data_processing.ingestion import DataIngestion

load_dotenv()

@click.group()
def cli():
    """Policy Navigator - Government Regulation Search System"""
    pass

@cli.command()
@click.option('--query', '-q', required=True, help='Policy query to search for')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def search(query, verbose):
    """Search for policy information"""
    if not os.getenv('AIXPLAIN_API_KEY'):
        click.echo("Error: AIXPLAIN_API_KEY not set. Please check your .env file.")
        return
    
    click.echo(f"Searching for: {query}")
    
    agent = PolicyNavigatorAgent()
    response = agent.query(query)
    
    click.echo("\n" + "="*50)
    click.echo("POLICY SEARCH RESULTS")
    click.echo("="*50)
    click.echo(response.get('output', 'No results found'))
    
    if verbose and 'intermediate_steps' in response:
        click.echo("\n" + "-"*30)
        click.echo("DETAILED STEPS:")
        click.echo("-"*30)
        for step in response['intermediate_steps']:
            click.echo(f"• {step}")

@cli.command()
@click.option('--policy-id', '-p', required=True, help='Policy ID to check (e.g., EO-14067)')
def status(policy_id):
    """Check policy status"""
    if not os.getenv('AIXPLAIN_API_KEY'):
        click.echo("Error: AIXPLAIN_API_KEY not set.")
        return
    
    click.echo(f"Checking status for: {policy_id}")
    
    agent = PolicyNavigatorAgent()
    status_info = agent.check_policy_status(policy_id)
    
    click.echo("\n" + "="*50)
    click.echo("POLICY STATUS")
    click.echo("="*50)
    click.echo(f"Policy ID: {status_info.get('policy_id', policy_id)}")
    click.echo(f"Status: {status_info.get('federal_status', {}).get('status', 'Unknown')}")
    
    if 'federal_status' in status_info:
        fs = status_info['federal_status']
        if 'title' in fs:
            click.echo(f"Title: {fs['title']}")
        if 'publication_date' in fs:
            click.echo(f"Publication Date: {fs['publication_date']}")
        if 'url' in fs:
            click.echo(f"URL: {fs['url']}")

@cli.command()
@click.option('--business-type', '-t', default='general', help='Type of business')
@click.option('--size', '-s', type=click.Choice(['small_business', 'large_business']), 
              default='small_business', help='Business size')
def compliance(business_type, size):
    """Analyze compliance requirements"""
    agent = PolicyNavigatorAgent()
    analysis = agent.analyze_compliance(business_type, size)
    
    click.echo("\n" + "="*50)
    click.echo("COMPLIANCE ANALYSIS")
    click.echo("="*50)
    click.echo(f"Business Type: {analysis['business_type']}")
    click.echo(f"Size: {analysis['size']}")
    
    click.echo("\nRequirements:")
    for regulation, requirements in analysis['requirements'].items():
        click.echo(f"\n{regulation.upper()}:")
        for req in requirements:
            click.echo(f"  • {req}")
    
    click.echo("\nDeadlines:")
    for deadline in analysis['deadlines']:
        click.echo(f"  • {deadline}")

@cli.command()
def setup():
    """Setup data ingestion and initial configuration"""
    click.echo("Setting up Policy Navigator...")
    
    # Create data directories
    os.makedirs('data/datasets', exist_ok=True)
    os.makedirs('data/scraped', exist_ok=True)
    
    # Initialize data ingestion
    ingestion = DataIngestion()
    
    click.echo("Loading sample policy data...")
    sample_data = ingestion.load_sample_policy_data()
    click.echo(f"Loaded {len(sample_data)} sample policies")
    
    click.echo("Scraping Federal Register...")
    fed_docs = ingestion.scrape_federal_register(limit=20)
    click.echo(f"Scraped {len(fed_docs)} Federal Register documents")
    
    click.echo("Setup complete!")

@cli.command()
def interactive():
    """Start interactive policy query session"""
    if not os.getenv('AIXPLAIN_API_KEY'):
        click.echo("Error: AIXPLAIN_API_KEY not set.")
        return
    
    click.echo("Policy Navigator Interactive Mode")
    click.echo("Type 'quit' to exit, 'help' for commands")
    click.echo("-" * 40)
    
    agent = PolicyNavigatorAgent()
    
    while True:
        try:
            query = input("\nPolicy Query> ").strip()
            
            if query.lower() in ['quit', 'exit']:
                break
            elif query.lower() == 'help':
                click.echo("Available commands:")
                click.echo("  - Ask any policy question")
                click.echo("  - 'status <policy-id>' - Check policy status")
                click.echo("  - 'compliance <business-size>' - Get compliance info")
                click.echo("  - 'quit' - Exit")
                continue
            elif query.startswith('status '):
                policy_id = query.replace('status ', '').strip()
                result = agent.check_policy_status(policy_id)
                click.echo(f"Status: {result}")
            elif query.startswith('compliance '):
                size = query.replace('compliance ', '').strip()
                result = agent.analyze_compliance('general', size)
                click.echo(f"Compliance: {result}")
            else:
                response = agent.query(query)
                click.echo(f"\nAnswer: {response.get('output', 'No response')}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            click.echo(f"Error: {e}")
    
    click.echo("\nGoodbye!")

if __name__ == '__main__':
    cli()