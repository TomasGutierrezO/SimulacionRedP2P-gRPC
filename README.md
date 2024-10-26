# Sistema P2P para Intercambio de Archivos

Este proyecto implementa una red peer-to-peer (P2P) diseñada para la simulación del intercambio de archivos entre nodos. La arquitectura emplea API REST para la comunicación con un servidor central y gRPC para la comunicación directa entre los peers.

## Objetivo

El sistema tiene como objetivo facilitar el intercambio eficiente de archivos entre usuarios predefinidos, proporcionando autenticación segura, búsqueda avanzada de archivos y descarga mediante comunicaciones optimizadas.

## Características

- **Red P2P Funcional**: Implementación de una red distribuida que permite la comunicación directa entre los peers.
- **API REST**: Gestiona la autenticación y la indexación de archivos a través de un servidor central.
- **gRPC**: Optimiza la transferencia de archivos entre los peers, minimizando la latencia.
- **Autenticación Segura**: Solo los usuarios predefinidos pueden acceder al sistema.
- **Simulación de Transferencia de Archivos**: El intercambio de archivos se simula mediante la transferencia de nombres de archivos entre peers.

## Funcionalidades Principales

1. **Inicio de Sesión**: Autenticación de usuarios predefinidos mediante credenciales.
2. **Cierre de Sesión**: Terminación segura de la sesión activa del usuario.
3. **Indexación de Archivos**: Actualización de los archivos disponibles para compartir en la red.
4. **Búsqueda de Archivos**: Búsqueda de archivos distribuidos en la red P2P.
5. **Descarga de Archivos**: Descarga de archivos desde otros peers conectados en la red.

## Requisitos Funcionales

- **Autenticación de Usuarios**: El sistema debe verificar credenciales contra una lista de usuarios predefinidos.
- **Gestión de Sesiones**: Permite que un usuario tenga solo una sesión activa simultáneamente.
- **Mantenimiento de Listas de Archivos**: Cada peer debe tener una lista actualizada de los archivos disponibles para compartir.

## Requisitos Técnicos

- **Lenguaje de Programación**: Python.
- **Framework REST**: Flask para la implementación del servidor central.
- **Comunicación Peer-to-Peer**: gRPC para conexiones rápidas y eficientes.
- **Almacenamiento**: Los datos de usuarios y archivos se almacenan en formato JSON.

## Requisitos No Funcionales

- **Escalabilidad**: El sistema debe poder manejar la adición de nuevos peers sin degradar significativamente el rendimiento.
- **Concurrencia**: El sistema debe soportar múltiples conexiones simultáneas entre peers utilizando gRPC.
- **Eficiencia**: Las comunicaciones entre peers deben ser optimizadas para reducir la latencia en la transferencia de archivos.

## Instrucciones de Instalación

### 1. Configuración del Servidor Central

1. En una terminal, navegue al directorio principal del proyecto.
2. Ejecute el siguiente comando para iniciar el servidor:

    ```bash
    python api_server.py
    ```

3. El servidor estará disponible en `http://127.0.0.1:5000`.

### 2. Configuración de los Peers

Para cada peer, siga los siguientes pasos:

1. Abra una nueva terminal y navegue al directorio correspondiente del peer (`/peer_n`, donde `n` es el número del peer).
2. Ejecute el servidor P2P con el siguiente comando:

    ```bash
    python p2p_server.py
    ```

### 3. Configuración del Cliente P2P

Para iniciar el cliente P2P:

1. Abra una nueva terminal y navegue al directorio del peer.
2. Ejecute el cliente con el siguiente comando:

    ```bash
    python p2p_client.py
    ```

3. Se mostrará el menú principal para interactuar con el sistema.

## Uso del Cliente

1. **Iniciar Sesión**: Seleccione la opción `1. Login` en el menú principal, luego ingrese el nombre de usuario y contraseña.
2. **Indexar Archivos**: Seleccione `3. Indexar Archivos` para actualizar la lista de archivos disponibles en la red.
3. **Buscar Archivos**: Seleccione `4. Buscar Archivo` e ingrese el nombre del archivo deseado.
4. **Descargar Archivos**: Tras una búsqueda exitosa, seleccione `5. Descargar Archivo` y elija el peer desde el cual descargar.
5. **Cerrar Sesión**: Seleccione `2. Logout` para cerrar su sesión de forma segura.

## Gestión de Archivos Compartidos

- **Añadir Archivos**: Para añadir nuevos archivos, edite el array `files` en el archivo `peer_config.json`. Reinicie el servidor P2P e indexe los archivos nuevamente.
- **Eliminar Archivos**: Para eliminar archivos, modifique el array `files` en `peer_config.json`, reinicie el servidor P2P e indexe nuevamente.

---

# P2P File Sharing System

This project implements a peer-to-peer (P2P) network designed to simulate file exchange between nodes. The architecture employs REST APIs for communication with a central server and gRPC for direct peer-to-peer communication.

## Objective

The system aims to facilitate efficient file sharing among predefined users, providing secure authentication, advanced file search, and download through optimized communication channels.

## Features

- **Functional P2P Network**: Implements a distributed system enabling direct communication between peers.
- **REST API**: Manages user authentication and file indexing through a central server.
- **gRPC**: Optimizes file transfer between peers, minimizing latency.
- **Secure Authentication**: Only predefined users can access the system.
- **File Transfer Simulation**: File exchange is simulated by transferring file names between peers.

## Main Functionalities

1. **User Login**: Authentication of predefined users via credentials.
2. **User Logout**: Secure termination of the active user session.
3. **File Indexing**: Update of the files available for sharing in the network.
4. **File Search**: Allows users to search for files distributed across the P2P network.
5. **File Download**: Allows users to download files from other peers connected to the network.

## Functional Requirements

- **User Authentication**: The system must verify credentials against a predefined list of users.
- **Session Management**: Allows only one active session per user.
- **File List Maintenance**: Each peer must maintain an updated list of files available for sharing.

## Technical Requirements

- **Programming Language**: Python.
- **REST Framework**: Flask for central server implementation.
- **Peer-to-Peer Communication**: gRPC for fast and efficient connections.
- **Storage**: User and indexed file data are stored in JSON format.

## Non-Functional Requirements

- **Scalability**: The system must handle the addition of new peers without significant performance degradation.
- **Concurrency**: The system must support multiple simultaneous connections between peers using gRPC.
- **Efficiency**: Peer-to-peer communications must be optimized to reduce latency in file transfers.

## Installation Guide

### 1. Central Server Setup

1. In a terminal, navigate to the project's main directory.
2. Run the following command to start the server:

    ```bash
    python api_server.py
    ```

3. The server will be available at `http://127.0.0.1:5000`.

### 2. Peer Setup

For each peer, follow these steps:

1. Open a new terminal and navigate to the corresponding peer directory (`/peer_n`, where `n` is the peer number).
2. Run the P2P server with the following command:

    ```bash
    python p2p_server.py
    ```

### 3. P2P Client Setup

To start the P2P client:

1. Open a new terminal and navigate to the peer directory.
2. Run the client with the following command:

    ```bash
    python p2p_client.py
    ```

3. The main menu will be displayed for system interaction.

## Client Usage

1. **Login**: Select option `1. Login` from the main menu, then enter the username and password.
2. **Index Files**: Select `3. Index Files` to update the list of available files in the network.
3. **Search Files**: Select `4. Search File` and enter the desired file name.
4. **Download Files**: After a successful search, select `5. Download File` and choose the peer from which to download.
5. **Logout**: Select `2. Logout` to securely end the session.

## Shared File Management

- **Add Files**: To add new files, edit the `files` array in the `peer_config.json` file. Restart the P2P server and re-index the files.
- **Remove Files**: To remove files, modify the `files` array in the `peer_config.json` file, restart the P2P server, and re-index the files.

---
