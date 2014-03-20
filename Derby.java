
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

public class Derby {
  private Connection connect = null;
  private Statement statement = null;
  private ResultSet resultSet = null;

  public Derby() throws Exception {
    try {

      Class.forName("org.apache.derby.jdbc.EmbeddedDriver").newInstance();
      connect = DriverManager
          .getConnection("jdbc:derby:derbyDB;create=true");
      {
        System.out.println("l");
        // PreparedStatement statement = connect.prepareStatement("create table USERS(name varchar(100),numvber int)");
        // statement.executeUpdate();
      }
      {
        System.out.println("2");
        PreparedStatement statement = connect.prepareStatement("insert into users values('a',1)");
        statement.executeUpdate();
      }
      {
        System.out.println("3");
        PreparedStatement statement = connect.prepareStatement("insert into users values('b',2)");
        statement.executeUpdate();
       }
       {
        PreparedStatement statement = connect.prepareStatement("SELECT * from USERS");
        resultSet = statement.executeQuery();
        while (resultSet.next()) {
          String user = resultSet.getString("name");
          String number = resultSet.getString("numvber");
          System.out.println("User: " + user);
          System.out.println("ID: " + number);
        }
      }
    } catch (Exception e) {
      throw e;
    } finally {
      close();
    }

  }

  private void close() {
    try {
      if (resultSet != null) {
        resultSet.close();
      }
      if (statement != null) {
        statement.close();
      }
      if (connect != null) {
        connect.close();
      }
    } catch (Exception e) {

    }
  }

  public static void main(String[] args) throws Exception {
    
    Derby dao = new Derby();
  }

} 