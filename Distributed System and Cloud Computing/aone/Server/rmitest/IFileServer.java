package rmitest;

import java.io.FileNotFoundException;
import java.io.IOException;

public interface IFileServer {
    public String read(String fileName) throws FileNotFoundException, IOException;
    public void create(String fileName) throws Exception;
    public void edit(String fileName, boolean append, String newContent) throws FileNotFoundException, IOException;
    public void delete(String fileName) throws IOException ;
    public void copy(String sourceFileName, String destinationFileName) throws FileNotFoundException, IOException ;
    public void move(String sourceFileName, String destinationFileName) throws IOException, FileNotFoundException ;
    public long size(String fileName) throws FileNotFoundException ; // returns size in bytes
    public long lastModified(String fileName) throws FileNotFoundException ; // returns timestamp
    public long lastAccessed(String fileName) throws FileNotFoundException ; // returns timestamp
}
