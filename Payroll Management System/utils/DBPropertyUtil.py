class DBPropertyUtil:
    @staticmethod
    def get_connection_string(config_file):
        connection_str = ""
        # Open the properties file
        with open(config_file, 'r') as file:
            for line in file:
                # Ignore empty lines and comments
                if line.strip() and not line.startswith('#'):
                    key, value = line.split('=')
                    # Append each key-value pair to the connection string
                    connection_str += f"{key.strip()}={value.strip()};"
        return connection_str
