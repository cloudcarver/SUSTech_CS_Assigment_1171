package rmitest;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface IFileServer extends Remote{
    /**
     * Read the content of a file into String.
     * @param fileName
     * @return the content of the file in String.
     * @throws FileNotFoundException throws when the file cannot be found by the name provided
     * @throws IOException throws when something went wrong during reading the file
     */
    public String read(String fileName) throws RemoteException, FileNotFoundException, IOException;
    
    
    
    /**
     * Create a file.
     * 
     * @param fileName the name of the created file
     * @throws Exception throws if something went wrong while creating the file. e.g. permission denied.
     */
    public void create(String fileName) throws RemoteException, Exception;
    
    
    
    /**
     * Edit a file. New content can be appened to the target file or used to
     * replace the original content. Deletion is not supported yet.
     * 
     * @param fileName the name of the file need to be edited
     * @param append true if you want to append something. false means replacing the original content with the new content
     * @param newContent the new content to append or write
     * @throws FileNotFoundException throws if the file not found
     * @throws IOException throws if something went wrong during editing the file
     */
    public void edit(String fileName, boolean append, String newContent) throws RemoteException, FileNotFoundException, IOException;
    
    
    
    /**
     * Delete a file.
     * 
     * @param fileName the name of the file need to be deleted
     * @throws IOException throws if something went wrong during deleting the file.
     */
    public void delete(String fileName) throws RemoteException, IOException ;
    
    
    
    /**
     * Copy the content of a file to new file.
     * 
     * @param sourceFileName the name of the file you copy from
     * @param destinationFileName the name of the file you paste to
     * @throws FileNotFoundException throws if the file is not found
     * @throws IOException throws if something went wrong during writing the new file or reading the src file.
     */
    public void copy(String sourceFileName, String destinationFileName) throws RemoteException, FileNotFoundException, IOException ;
    
    
    
    /**
     * Move (rename) a file.
     * 
     * @param sourceFileName the name of the file need to be moved
     * @param destinationFileName the destination moving to
     * @throws IOException throws if something went wrong during when calling the renameTo() method of File object
     * @throws FileNotFoundException throws if the source file is not found
     */
    public void move(String sourceFileName, String destinationFileName) throws RemoteException, IOException, FileNotFoundException ;
    
    
    
    /**
     * Get the length (size) of a file in bytes.
     * 
     * @param fileName the name of the file you want to know its length (size)
     * @return the length (size) of the file in bytes
     * @throws FileNotFoundException throws if the file is not found.
     */
    public long size(String fileName) throws RemoteException, FileNotFoundException ; // returns size in bytes
    
    
    
    /**
     * Get the last modified time (in UNIX timestamp) of a file.
     * 
     * @param fileName the name of the file you want to know its last modified time.
     * @return the UNIX timestamp of the last modified time
     * @throws FileNotFoundException throws if the file is not found.
     */
    public long lastModified(String fileName) throws RemoteException, FileNotFoundException ; // returns timestamp
    
    
    
    /**
     * Get the last accessed time (in UNIX timestamp) of a file.
     * The file is considered as being accesed when one of the following methods is called:
     *   1) create
     *   2) read
     *   3) edit
     * 
     * @param fileName the name of the file you want to know its last accessed time.
     * @return the UNIX timestamp of the last accessed time of this file
     * @throws FileNotFoundException throws if the file is not found.
     */
    public long lastAccessed(String fileName) throws RemoteException, FileNotFoundException ; // returns timestamp
   
   
   
    /**
     * List all the file (the last name of its abtract path) in the current directory (./).
     * 
     * @return a string contains all the name of the files in current directory (./)
     * @throws RemoteException throws when something went wrong during RMI
     */
    public String list() throws RemoteException;
}
