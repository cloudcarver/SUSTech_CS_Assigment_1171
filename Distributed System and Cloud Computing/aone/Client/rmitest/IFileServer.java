package rmitest;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface IFileServer extends Remote{
    public String read(String fileName) throws RemoteException, FileNotFoundException, IOException;
    public void create(String fileName) throws RemoteException, Exception;
    public void edit(String fileName, boolean append, String newContent) throws RemoteException, FileNotFoundException, IOException;
    public void delete(String fileName) throws RemoteException, IOException ;
    public void copy(String sourceFileName, String destinationFileName) throws RemoteException, FileNotFoundException, IOException ;
    public void move(String sourceFileName, String destinationFileName) throws RemoteException, IOException, FileNotFoundException ;
    public long size(String fileName) throws RemoteException, FileNotFoundException ; // returns size in bytes
    public long lastModified(String fileName) throws RemoteException, FileNotFoundException ; // returns timestamp
    public long lastAccessed(String fileName) throws RemoteException, FileNotFoundException ; // returns timestamp
    public String list() throws RemoteException;
}
