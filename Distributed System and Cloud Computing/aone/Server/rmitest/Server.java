package rmitest;

import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
public class Server{
    
    private Registry registry;

    public Server(int port) throws RemoteException{
        registry = LocateRegistry.createRegistry(port);
    }

    public void addFileSystemInstance(String name){
        try{
            registry.rebind(name, new FileServer());
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws RemoteException{
        Server server = new Server(51800);
        server.addFileSystemInstance("test1");
        System.out.println("Server is listening.");
    }
}