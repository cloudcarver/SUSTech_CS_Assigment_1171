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

    public void create(String fileName) throws Exception {
        File file = new File(fileName);
        if(file.exists()){
            throw new Exception("File already exists: " + fileName);
        }else{
            file.createNewFile();
        }
        updateLastAccessTime(fileName);
    }

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

    public void delete(String fileName) throws IOException {
        File file = new File(fileName);
        file.delete();
    }

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

    public void move(String sourceFileName , String destinationFileName) throws IOException, FileNotFoundException {
        File srcFile = new File(sourceFileName);
        if( ! srcFile.exists() ){
            throw new FileNotFoundException("No such file: " + srcFile.getName());
        }
        srcFile.renameTo(new File(destinationFileName));
    }

    public long size(String fileName) throws FileNotFoundException {
        File file = new File(fileName);
        if( ! file.exists() ){
            throw new FileNotFoundException("No such file: " + fileName);
        }
        return file.length();
    } // returns size in bytes

    public long lastModified(String fileName) throws FileNotFoundException {
        File file = new File(fileName);
        if( ! file.exists() ){
            throw new FileNotFoundException("No such file: " + fileName);
        }
        return file.lastModified();
    }// returns timestamp

    public long lastAccessed(String fileName) throws FileNotFoundException {
    	File file = new File(fileName);
        if( ! file.exists() ){
            throw new FileNotFoundException("No such file: " + fileName);
        }
    	return lastAccessedLog.get(fileName);
    } // returns timestamp
    
    public String list() throws RemoteException{
    	StringBuilder sb = new StringBuilder();
    	for(String name : new File("./").list()) {
    		sb.append(name + " ");
    	}
    	return sb.toString();
    }
}

