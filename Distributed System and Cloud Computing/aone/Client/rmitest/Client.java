package rmitest;

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Client{
    private Registry registry;

    public Client(String host, int port){
        try{
            registry = LocateRegistry.getRegistry(host, port);
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public IFileServer getFileSystem(String objectName){
        try{
            return (IFileServer) registry.lookup(objectName);
        }catch(Exception e){
            e.printStackTrace();
        }
        return null;
    }

    public static void main(String[] args) throws Exception{
        Client client = new Client("127.0.0.1", 51800);
        IFileServer fileSystem = client.getFileSystem("test1");
        
        fileSystem.create("test.txt");
    }

}