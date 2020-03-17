package rmitest;

import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.Scanner;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
class Command{
	
	private String[] args;
	private HashMap<String, String> options;
	private String command;
	
	Command(String command){
		if(command.contains(">")) {
			
			this.command = "edit";
			args = new String[3];
			
			if(command.contains(">>>")) {
				String[] items = command.split(">>>");
				args[2] = "\n" + items[0];
				args[1] = "true";
				args[0] = items[1].trim();
			}else if(command.contains(">>")) {
				String[] items = command.split(">>");
				args[2] = items[0];
				args[1] = "true";
				args[0] = items[1].trim();
			}else {
				String[] items = command.split(">");
				args[2] = items[0];
				args[1] = "false";
				args[0] = items[1].trim();
			}
			
		}else {
			options = new HashMap<>();
			
			String[] raw = command.split(" ");
			this.command = raw[0];
			args = new String[raw.length - 1];
			
			int argc = 0;
			for(int i = 1; i < raw.length; i++) {
				if(raw[i].contains("-")) {
					options.put(raw[i], raw[++i]);
				}else {
					args[argc++] = raw[i];
				}
			}
		}
		
	}
	/**
	 * Get the all the options in the command.
	 * @return the map contains all the options pair.
	 */
	public HashMap<String, String> getOptions(){
		return options;
	}
	

	/**
	 * Get an argument in this command
	 * @param index the order number of this argument
	 * @return the string representation of this argument
	 */
	public String getArg(int index) {
		return args[index];
	}
	
	/**
	 * Get an option value in this command.
	 * An option pair is constructed like this:
	 * time -a t.txt
	 * <"-a", "t.txt">
	 * @param key the option
	 * @return the value of this option
	 */
	public String getOption(String key) {
		return options.get(key);
	}
	
	/**
	 * The service called in this command. For example,
	 * for the command `time -a t.txt`, the service is "time"
	 * @return the service of the command required
	 */
	public String getCommand() {
		return command;
	}
	
	public String toString() {
		return "command: " + command + " options: " + options + " args: " + Arrays.toString(args);
	}
}

public class Client {
    private Registry registry;
    private IFileServer fileSystem;

	/**
	 * Construct a client connected to the remote server providing remote method 
	 * innvocation services.
	 * 
	 * @param host the address of the server
	 * @param port the port of the server opened for RMI service
	 */
    public Client(String host, int port){
        try{
            registry = LocateRegistry.getRegistry(host, port);
        }catch(Exception e){
            e.printStackTrace();
        }
        fileSystem = getFileSystem("remoteFileServer");
    }

	/**
	 * Get an remote object instance via lookup method
	 * 
	 * @param objectName the name of the remote object registed in the registry. 
	 * @return the remote reference or null if the name is incorrect.
	 */
    public IFileServer getFileSystem(String objectName){
        try{
            return (IFileServer) registry.lookup(objectName);
        }catch(Exception e){
            e.printStackTrace();
        }
        return null;
    }
	/**
	 * Read the content of a file to standard output
	 * @param fileName the name of the file you want to read
	 */
    public void read(String fileName) {
    	try {
    		System.out.println(fileSystem.read(fileName));
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
	
	/**
	 * Create a file in the remote server
	 * @param fileName the name of the file created
	 */
    public void create(String fileName) {
    	try {
    		fileSystem.create(fileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
	
	/**
	 * Edit a file in the remote server.
	 * @param fileName the name of the file edited
	 * @param append true if you want to append the content to the original content.
	 *               false if you want to replace the original content by the new content.
	 * @param newContent the content you want to write to the file
	 */
    public void edit(String fileName, boolean append, String newContent) {
    	try {
    		fileSystem.edit(fileName, append, newContent);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
	
	/**
	 * delete a file in remote server
	 * @param fileName the name of the file you want to delete
	 */
    public void delete(String fileName) {
    	try {
    		fileSystem.delete(fileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
	
	/**
	 * Copy a file in the remote server to another place in the remote server.
	 * @param sourceFileName the name of the file you copy from
	 * @param destinationFileName the name of the file you paste to
	 */
    public void copy(String sourceFileName, String destinationFileName) {
    	try {
    		fileSystem.copy(sourceFileName, destinationFileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
	}
	
	/**
	 * Rename a file in the remote server.
	 * @param sourceFileName the orginal name
	 * @param destinationFileName the name you want to rename to
	 */
    public void move(String sourceFileName, String destinationFileName) {
    	try {
    		fileSystem.move(sourceFileName, destinationFileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
	}
	
	/**
	 * Print to size (length) of a file in the remote server in bytes to standard output
	 * @param fileName the name of the file you want to know its size
	 */
    public void size(String fileName) {
    	try {
    		System.out.println(fileSystem.size(fileName) + "bytes");
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
	}
	
	/**
	 * Print the datetime of the last modified time of a file
	 * @param fileName the name of the file you want to know its last modified time
	 */
    public void lastModified(String fileName) {
    	try {
    		System.out.println(new Date(fileSystem.lastModified(fileName)));
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
	}
	
	/**
	 * Print the datetime of the last accessed time of a file
	 * @param fileName the name of the file you want to know its last accessed time
	 */
    public void lastAccessed(String fileName) {
    	try {
    		System.out.println(new Date(fileSystem.lastAccessed(fileName)));
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
	}
	
	/**
	 * Print all the names of the files in the remote server to the standard output.
	 */
    public void list() {
    	try {
			System.out.println(fileSystem.list());
		} catch (RemoteException e) {
			System.out.println(e.getMessage());
		}
    }

	/**
	 * Handle user's input
	 * @param comm the Command object constructed from user's input
	 * @return false if user's input is `exit`; otherwise, it always be true.
	 */
    public boolean handleCommand(Command comm) {
    	String command = comm.getCommand();
    	if(command.equals("cat")) {
    		read(comm.getArg(0));
    	}else if(command.equals("exit")) {
    		return false;
    	}else if(command.equals("ls")) {
    		list();
    	}else if(command.equals("new")) {
    		create(comm.getArg(0));
    	}else if(command.equals("rm")) {
    		delete(comm.getArg(0));
    	}else if(command.equals("cp")) {
    		copy(comm.getArg(0), comm.getArg(1));
    	}else if(command.equals("mv")) {
    		move(comm.getArg(0), comm.getArg(1));
    	}else if(command.equals("time")) {
    		if(comm.getOptions().containsKey("-m")) {
    			lastAccessed(comm.getOptions().get("-m"));
    		}
    		if(comm.getOptions().containsKey("-a")) {
    			lastAccessed(comm.getOptions().get("-a"));
    		}
    		if(! (comm.getOptions().containsKey("-a") || comm.getOptions().containsKey("-m"))){
    			System.out.println("Invalid options :" + comm.getOptions().keySet());
    		}
    	}else if(command.equals("size")) {
    		size(comm.getArg(0));
    	}else if(command.equals("help") || command.equals("?")) {
    		
    		System.out.println("Simple remote rmi server.\n"
    				+ "Usage: command <options> [args]\n"
    				+ "ls: list all file\n"
    				+ "new [file name]: create a new file\n"
    				+ "rm [file name]: delete a file\n"
    				+ "cp [src file] [dst file]: copy a file to dst path\n"
    				+ "mv [src file] [dst file]: move a file to dst path\n"
    				+ "time <-a | -m> [file name]: show the time information of a file\n"
    				+ "    -a : last accessed time\n"
    				+ "    -m : last modified time\n");
    		
    	}else if(command.equals("edit")) {
    		edit(comm.getArg(0), comm.getArg(1).equals("true"), comm.getArg(2));
    	}else if(command.equals("")) {
    	
    	}else {
    		System.out.println("Invalid arguments.");
    	}
    	return true;
    }
    
    public static void main(String[] args) throws Exception{
        Client client = new Client("localhost", 51800);
              
        Scanner scan = new Scanner(System.in);
        while(client.handleCommand(new Command(scan.nextLine()))) {
        	
        }
        System.out.println("bye");
        scan.close();
    }
}