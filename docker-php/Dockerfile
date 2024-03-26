# PHP Apache base
FROM php:8.2-apache

# Instalar dependencias
RUN apt-get update \
    && apt-get install -y \
        libcurl4-openssl-dev \
        pkg-config \
        libssl-dev \
        zip \
        git

# Instalar mongodb
RUN pecl install mongodb \
    && docker-php-ext-enable mongodb

# Instala composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Permisos composer
RUN chmod +x /usr/local/bin/composer
