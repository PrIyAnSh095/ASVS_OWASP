# Solution Guide

To satisfy ASVS 4.3.2, disable introspection in production.

1. Locate your GraphQL server configuration.
2. Check the framework documentation for the introspection setting.
3. Ensure it is conditionally tied to the environment variables (e.g., enabled if `NODE_ENV=development`, disabled if `NODE_ENV=production`).

Example for Apollo Server:
```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production'
});
```
