FROM public.ecr.aws/bitnami/node:14.17.0-prod as builder

WORKDIR /app
COPY . /app

# production environment

FROM public.ecr.aws/nginx/nginx:1.21-alpine
COPY --from=builder /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
