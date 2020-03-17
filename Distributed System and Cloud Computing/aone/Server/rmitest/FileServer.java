package rmitest;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.util.Date;
import java.util.HashMap;
import java.util.NoSuchElementException;
import java.util.StringTokenizer;
import java.util.Map.Entry;

public class FileServer extends UnicastRemoteObject implements IFileServer{
    
    private static final long serialVersionUID = 1L;
    private static final String logName = ".fileServerAccessLog";

    private HashMap<String, Long> lastAccessedLog;

    protected FileServer() throws RemoteException{
        super();
        try{
            loadAccessLog();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    /**
     * Make sure the log in memory will be saved in local file. 
     */
    @Override
    public void finalize(){
        try{
            writeAccessLog();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    private void updateLastAccessTime(String name){
    	long currentTime = System.currentTimeMillis();
        lastAccessedLog.put(name, currentTime);
    }

    /**
     * Write the content in loadAccessedLog into a log file.
     * 
     * @throws FileNotFoundException cannot file the log file in current directory
     * @throws IOException something went wrong when writing the log file
     */
    private void writeAccessLog() throws FileNotFoundException, IOException {
        System.out.println("Writing access log...");
        File file = new File(logName);
        FileOutputStream fos = new FileOutputStream(file);
        StringBuilder sb = new StringBuilder();

        for(Entry<String, Long> entry : lastAccessedLog.entrySet()){
            sb.append(entry.getKey() + " " + String.valueOf(entry.getValue()) + "\n");
        }

        fos.write(sb.toString().getBytes());
        fos.close();
        System.out.println("Successfully save access log.");
    }

    /**
     * This method will load the access time information in the log file into memory (HashMap)
     * If it is the firt time to run the file server, this method will create a new log file.
     * And the last access time of files is their last modified time.
     * 
     * @throws IOException something wrong when loading or writing the log file.
     * @throws NoSuchElementException The format of the log file is incorrect.
     */
    private void loadAccessLog() throws IOException, NoSuchElementException{

        lastAccessedLog = new HashMap<String, Long>();

        File file = new File(logName);
        try{
            if( ! file.exists()){
                file.createNewFile();
                File currentDir = new File("./");
                for(File f : currentDir.listFiles()){
                    lastAccessedLog.put(f.getName(), f.lastModified());
                }
                writeAccessLog();
                return;
            }
        }catch(IOException e){
            throw new IOException("Cannot create log file in file server. This may cause incorrect access time.");
        }

        BufferedReader buf = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
        String line = null;
        StringTokenizer st;

        try{
            while((line = buf.readLine()) != null){
                st = new StringTokenizer(line);
                lastAccessedLog.put(st.nextToken(), Long.valueOf(st.nextToken()));
            }
        }catch(IOException e2){
            buf.close();
            throw new IOException("Cannot access log file in file server. This may cause incorrect access time.");
        }catch(NoSuchElementException ne){
            buf.close();
            throw new NoSuchElementException("Invalid log format. This may cause incorrect access time.");
        }
        buf.close();
    }

    /**
     * Read the content of a file into String.
     * @param fileName
     * @return the content of the file in String.
     * @throws FileNotFoundException throws when the file cannot be found by the name provided
     * @throws IOException throws when something went wrong during reading the file
     */
    public String read(String fileName) throws FileNotFoundException, IOException{
        BufferedReader buf = new BufferedReader(new InputStreamReader(new FileInputStream(new File(fileName))));
        String line = null;
        StringBuilder sb = new StringBuilder();
        try{
            while( (line = buf.readLine()) != null){
                sb.append(line + "\n");
            }
        }catch(IOException io){
            buf.close();
            throw io;
        }
        buf.close();

        updateLastAccessTime(fileName);
        return sb.toString();
    }

    /**
     * Create a file.
     * 
     * @param fileName the name of the created file
     * @throws Exception throws if something went wrong while creating the file. e.g. permission denied.
     */
    public void create(String fileName) throws Exception {
        File file = new File(fileName);
        if(file.exists()){
            throw new Exception("File already exists: " + fileName);
        }else{
            file.createNewFile();
        }
        updateLastAccessTime(fileName);
    }


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
    public void edit(String fileName, boolean append, String newContent) throws FileNotFoundException, IOException {
        File file = new File(fileName);
        if( ! file.exists()){
            throw new FileNotFoundException("No such file: " + fileName);
        }

        FileOutputStream fos = null;
        try{
            fos = new FileOutputStream(file, append);
            fos.write(newContent.getBytes());
        }catch(IOException ie){
            fos.close();
            throw new IOException("Something went wrong while writing the file");
        }
        updateLastAccessTime(fileName);
        fos.close();
    }

    /**
     * Delete a file.
     * 
     * @param fileName the name of the file need to be deleted
     * @throws IOException throws if something went wrong during deleting the file.
     */
    public void delete(String fileName) throws IOException {
        File file = new File(fileName);
        file.delete();
    }

    /**
     * Copy the content of a file to new file.
     * 
     * @param sourceFileName the name of the file you copy from
     * @param destinationFileName the name of the file you paste to
     * @throws FileNotFoundException throws if the file is not found
     * @throws IOException throws if something went wrong during writing the new file or reading the src file.
     */
    public void copy(String sourceFileName , String destinationFileName) throws FileNotFoundException, IOException {
        BufferedReader buf = new BufferedReader(new InputStreamReader(new FileInputStream(new File(sourceFileName))));    
        StringBuilder sb = new StringBuilder();
        String line = null;
        try{
            while((line = buf.readLine()) != null){
                sb.append(line + "\n");
            }
        }catch(IOException ie){
            buf.close();
            throw ie;
        }
        buf.close();

        File dstFile = new File(destinationFileName);
        if( ! dstFile.exists()){
            dstFile.createNewFile();
        }
        FileOutputStream fos = new FileOutputStream(dstFile);
        fos.write(sb.toString().getBytes());
        fos.close();
    }

    /**
     * Move (rename) a file.
     * 
     * @param sourceFileName the name of the file need to be moved
     * @param destinationFileName the destination moving to
     * @throws IOException throws if something went wrong during when calling the renameTo() method of File object
     * @throws FileNotFoundException throws if the source file is not found
     */
    public void move(String sourceFileName , String destinationFileName) throws IOException, FileNotFoundException {
        File srcFile = new File(sourceFileName);
        if( ! srcFile.exists() ){
            throw new FileNotFoundException("No such file: " + srcFile.getName());
        }
        srcFile.renameTo(new File(destinationFileName));
    }

    /**
     * Get the length (size) of a file in bytes.
     * 
     * @param fileName the name of the file you want to know its length (size)
     * @return the length (size) of the file in bytes
     * @throws FileNotFoundException throws if the file is not found.
     */
    public long size(String fileName) throws FileNotFoundException {
        File file = new File(fileName);
        if( ! file.exists() ){
            throw new FileNotFoundException("No such file: " + fileName);
        }
        return file.length();
    } // returns size in bytes

    /**
     * Get the last modified time (in UNIX timestamp) of a file.
     * 
     * @param fileName the name of the file you want to know its last modified time.
     * @return the UNIX timestamp of the last modified time
     * @throws FileNotFoundException throws if the file is not found.
     */
    public long lastModified(String fileName) throws FileNotFoundException {
        File file = new File(fileName);
        if( ! file.exists() ){
            throw new FileNotFoundException("No such file: " + fileName);
        }
        return file.lastModified();
    }// returns timestamp


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
    public long lastAccessed(String fileName) throws FileNotFoundException {
    	File file = new File(fileName);
        if( ! file.exists() ){
            throw new FileNotFoundException("No such file: " + fileName);
        }
    	return lastAccessedLog.get(fileName);
    } // returns timestamp
    
    /**
     * List all the file (the last name of its abtract path) in the current directory (./).
     * 
     * @return a string contains all the name of the files in current directory (./)
     * @throws RemoteException throws when something went wrong during RMI
     */
    public String list() throws RemoteException{
    	StringBuilder sb = new StringBuilder();
    	for(String name : new File("./").list()) {
    		sb.append(name + " ");
    	}
    	return sb.toString();
    }
}

