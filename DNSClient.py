import dns.resolver
import dns.exception

# Set the IP address of the local DNS server and a public DNS server
local_host_ip = "127.0.0.1"
real_name_server = "8.8.8.8"  # Google's public DNS; you can change to "1.1.1.1" (Cloudflare) if you prefer

# Create a list of domain names to query - use the same list from the DNS Server
domainList  = ['example.com.','safebank.com.','google.com.','nyu.edu.','legitsite.com.']

# Define a function to query the local DNS server for the IP address of a given domain name
def query_local_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [local_host_ip]
    try:
        answers = resolver.resolve(domain, question_type)  # provide the domain and question_type
        ip_address = answers[0].to_text()
        return ip_address
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
        return ""  # return empty string on failure


# Define a function to query a public DNS server for the IP address of a given domain name
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]
    try:
        answers = resolver.resolve(domain, question_type)  # provide the domain and question_type
        ip_address = answers[0].to_text()
        return ip_address
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
        return ""  # return empty string on failure


# Define a function to compare the results from the local and public DNS servers for each domain name in the list
def compare_dns_servers(domainList, question_type):
    for domain_name in domainList:
        local_ip_address = query_local_dns_server(domain_name, question_type)
        public_ip_address = query_dns_server(domain_name, question_type)
        if local_ip_address != public_ip_address:
            return False
    return True


# Define a function to print the results from querying both the local and public DNS servers for each domain name in the domainList
def local_external_DNS_output(question_type):
    print("Local DNS Server")
    for domain_name in domainList:
        ip_address = query_local_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address if ip_address else 'NO ANSWER'}")

    print("\nPublic DNS Server")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address if ip_address else 'NO ANSWER'}")


def exfiltrate_info(domain, question_type):  # testing method for part 2
    data = query_local_dns_server(domain, question_type)
    return data


if __name__ == '__main__':
    # Set the type of DNS query to be performed
    question_type = 'A'

    # Call the function to print the results from querying both DNS servers
    # Uncomment to print all domain results:
    # local_external_DNS_output(question_type)

    # Call the function to compare the results from both DNS servers and print the result
    result = compare_dns_servers(domainList, question_type)
    print("All domains matched between local and public DNS:" , result)

    # Example: query a single domain from local DNS (prints the local server's answer)
    result = query_local_dns_server('nyu.edu.', question_type)
    print("Local DNS answer for nyu.edu.:", result)

    # Example exfiltrate_info usage (for testing in Part 2)
    # print(exfiltrate_info('example.com.', question_type))
