FROM node:22-alpine
RUN apk add --no-cache curl
COPY ./ /app/
WORKDIR /app
RUN npm install
RUN npm run build
# CMD ["node", "dist/server.js"] 
CMD ["node", "-r", "./dist/instrumentation.js", "dist/server.js"] 