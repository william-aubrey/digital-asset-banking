# Snowflake Pseudo-Admin Role Creation

## Overview

This context file provides guidance on creating a pseudo-admin role in Snowflake that has delegated powers from both `SYSADMIN` and `SECURITYADMIN` without requiring full `ACCOUNTADMIN` privileges. This approach allows for more granular access control while still providing necessary administrative capabilities.

## Best Practices

- Always follow the principle of least privilege when creating roles
- Document all custom roles and their permissions
- Regularly audit role permissions to ensure they remain appropriate
- Use descriptive role names that indicate their purpose
- Include comments when creating roles to document their intended use

## Method for Creating a Pseudo-Admin Role

This process should be executed by a user with `ACCOUNTADMIN` privileges.

### 1. Create the Custom Role

First, create the role itself using the `USERADMIN` role:

```sql
USE ROLE USERADMIN;
CREATE ROLE <pseudo_admin_role> COMMENT = 'Custom admin role for managing users, roles, and objects.';
```

### 2. Grant Object Creation Privileges

Next, switch to `SYSADMIN` to grant privileges for creating top-level objects:

```sql
USE ROLE SYSADMIN;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE <pseudo_admin_role>;
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE <pseudo_admin_role>;
```

### 3. Grant Security Privileges

Switch to `SECURITYADMIN` to grant privileges for creating users and roles:

```sql
USE ROLE SECURITYADMIN;
GRANT CREATE USER ON ACCOUNT TO ROLE <pseudo_admin_role>;
GRANT CREATE ROLE ON ACCOUNT TO ROLE <pseudo_admin_role>;
```

### 4. Grant the "Power" Privilege

Finally, grant the critical `MANAGE GRANTS` privilege:

```sql
USE ROLE SECURITYADMIN;
GRANT MANAGE GRANTS ON ACCOUNT TO ROLE <pseudo_admin_role>;
```

## Implementation in Matillion

When implementing this in Matillion pipelines:

1. Create an orchestration pipeline specifically for RBAC setup
2. Use SQL Executor components to execute each step in sequence
3. Consider using variables for role names to make the pipeline reusable
4. Add appropriate error handling and logging
5. Document the purpose of each component in the pipeline

## Example Use Case

A common implementation is creating a service account role like `<pseudo_admin_role>` that has sufficient privileges to perform ETL operations without having full administrative access to the Snowflake account.

## Security Considerations

- The `MANAGE GRANTS` privilege is powerful and should be granted carefully
- Consider implementing additional restrictions on the pseudo-admin role as needed
- Regularly audit the actions performed by users with this role
- Consider implementing custom resource monitors to limit resource usage

## References

- [Snowflake Documentation on Access Control](https://docs.snowflake.com/en/user-guide/security-access-control.html)
- [Snowflake Role-Based Access Control](https://docs.snowflake.com/en/user-guide/security-access-control-overview.html)
- [Snowflake System-Defined Roles](https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html)