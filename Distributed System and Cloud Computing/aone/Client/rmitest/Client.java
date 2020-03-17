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
	
	public HashMap<String, String> getOptions(){
		return options;
	}
	
	public String getArg(int index) {
		return args[index];
	}
	
	public String getOption(String key) {
		return options.get(key);
	}
	
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

    public Client(String host, int port){
        try{
            registry = LocateRegistry.getRegistry(host, port);
        }catch(Exception e){
            e.printStackTrace();
        }
        fileSystem = getFileSystem("remoteFileServer");
    }

    public IFileServer getFileSystem(String objectName){
        try{
            return (IFileServer) registry.lookup(objectName);
        }catch(Exception e){
            e.printStackTrace();
        }
        return null;
    }
    
    public void read(String fileName) {
    	try {
    		System.out.println(fileSystem.read(fileName));
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    
    public void create(String fileName) {
    	try {
    		fileSystem.create(fileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    
    public void edit(String fileName, boolean append, String newContent) {
    	try {
    		fileSystem.edit(fileName, append, newContent);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    
    public void delete(String fileName) {
    	try {
    		fileSystem.delete(fileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    
    public void copy(String sourceFileName, String destinationFileName) {
    	try {
    		fileSystem.copy(sourceFileName, destinationFileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    public void move(String sourceFileName, String destinationFileName) {
    	try {
    		fileSystem.move(sourceFileName, destinationFileName);
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    public void size(String fileName) {
    	try {
    		System.out.println(fileSystem.size(fileName) + "bytes");
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    public void lastModified(String fileName) {
    	try {
    		System.out.println(new Date(fileSystem.lastModified(fileName)));
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    public void lastAccessed(String fileName) {
    	try {
    		System.out.println(new Date(fileSystem.lastAccessed(fileName)));
    	}catch(Exception e) {
    		System.out.println(e.getMessage());
    	}
    }
    public void list() {
    	try {
			System.out.println(fileSystem.list());
		} catch (RemoteException e) {
			System.out.println(e.getMessage());
		}
    }

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