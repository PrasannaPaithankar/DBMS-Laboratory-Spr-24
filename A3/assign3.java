/*
 *  Author: Prasanna Paithankar (21CS30065)
 *  Date: 30/08/2021
 *  Course: Database Management Systems Lab
 *  File: assign3.java
 */

import java.util.*;

public class assign3 
{
    public static void main(String[] args) throws Exception
    {
        // Load the PostgreSQL JDBC driver
        Class.forName("org.postgresql.Driver");

        // Connect to the database
        String url = "jdbc:postgresql://localhost:5432/prasanna";
        Properties props = new Properties();
        props.setProperty("user","prasanna");
        props.setProperty("password","prasanna");
        java.sql.Connection conn = java.sql.DriverManager.getConnection(url, props);
        java.sql.Statement stmt = conn.createStatement();
        
        // Setup the scanner
        Scanner input = new Scanner(System.in);
        
        System.out.println("Welcome to the JDBC Query Processor!");
        System.out.println("\nQueries:");
        System.out.println("1. Roll number and name of all the students who are managing the \"Megaevent\"");
        System.out.println("2. Roll number and name of all the students who are managing the \"Megaevent\" as an \"Secretary\"");
        System.out.println("3. Name of all participants from the college \"IITB\" in \"Megaevent\"");
        System.out.println("4. Name of all colleges who have at least one participant in \"Megaevent\"");
        System.out.println("5. Name of all events which is managed by a \"Secretary\"");
        System.out.println("6. Name of all the \"CSE\" department student volunteers of \"Megaevent\"");
        System.out.println("7. Name of all the events which have at least one volunteer from \"CSE\"");
        System.out.println("8. Name of the college with the largest number of participants in \"Megaevent\"");
        System.out.println("9. Name of the college with the largest number of participants overall");
        System.out.println("10. Name of the department with the largest number of volunteers in  all the events which has at least one participant from \"IITB\"");
        System.out.println("11. Roll number and name of all the students who are managing the event <input>");
            
        while (true)
        {
            System.out.println("\nEnter your choice:");
            int choice = input.nextInt();
            System.out.println("\nOutput:\n");

            // Run appropriate query based on user input
            switch(choice)
            {
                case 1: // Roll number and name of all the students who are managing the "Megaevent"
                    java.sql.ResultSet rs = stmt.executeQuery("SELECT S.Roll, S.Name FROM Student S, Student_Event SE, Event E WHERE S.Roll = SE.Roll AND SE.EID = E.EID AND E.EName = 'Megaevent'");
                    System.out.println("Roll\tName");
                    System.out.println("----\t----");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1) + "\t" + rs.getString(2));
                    }
                    break;

                case 2: // Roll number and name of all the students who are managing the "Megaevent" as an "Secretary"
                    rs = stmt.executeQuery("SELECT S.Roll, S.Name FROM Student S, Student_Event SE, Event E, Role R WHERE S.Roll = SE.Roll AND SE.EID = E.EID AND E.EName = 'Megaevent' AND S.RID = R.RID AND R.Rname = 'Secretary'");
                    System.out.println("Roll\tName");
                    System.out.println("----\t----");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1) + "\t" + rs.getString(2));
                    }
                    break;

                case 3: // Name of all participants from the college "IITB" in "Megaevent"
                    rs = stmt.executeQuery("SELECT P.Name FROM Participant P, Event_Participant VEP, Event E WHERE P.PID = VEP.PID AND VEP.EID = E.EID AND E.EName = 'Megaevent' AND P.CName = 'IITB'");
                    System.out.println("Name");
                    System.out.println("----");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;
                    
                case 4: // Name of all colleges who have at least one participant in "Megaevent"
                    rs = stmt.executeQuery("SELECT DISTINCT P.CName FROM Participant P, Event_Participant VEP, Event E WHERE P.PID = VEP.PID AND VEP.EID = E.EID AND E.EName = 'Megaevent'");
                    System.out.println("College");
                    System.out.println("-------");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;

                case 5: // Name of all events which is managed by a "Secretary"
                    rs = stmt.executeQuery("SELECT E.EName FROM Event E, Student S, Student_Event SE, Role R WHERE E.EID = SE.EID AND SE.Roll = S.Roll AND S.RID = R.RID AND R.Rname = 'Secretary'");
                    System.out.println("Event");
                    System.out.println("-----");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;

                case 6: // Name of all the "CSE" department student volunteers of "Megaevent"
                    rs = stmt.executeQuery("SELECT S.Name FROM Student S, Volunteer V, Event E, Student_Event SE WHERE S.Roll = V.Roll AND V.EID = E.EID AND E.EName = 'Megaevent' AND S.Dept = 'CSE' AND S.Roll = SE.Roll AND SE.EID = E.EID");
                    System.out.println("Name");
                    System.out.println("----");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;

                case 7: // Name of all the events which have at least one volunteer from "CSE"
                    rs = stmt.executeQuery("SELECT E.EName FROM Event E, Student S, Volunteer V WHERE E.EID = V.EID AND V.Roll = S.Roll AND S.Dept = 'CSE'");
                    System.out.println("Event");
                    System.out.println("-----");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;

                case 8: // Name of the college with the largest number of participants in "Megaevent"
                    rs = stmt.executeQuery("SELECT P.CName FROM Participant P JOIN Event_Participant VEP ON P.PID = VEP.PID JOIN Event E ON VEP.EID = E.EID WHERE E.EName = 'Megaevent' GROUP BY P.CName HAVING COUNT(*) = ( SELECT MAX(cnt) FROM ( SELECT COUNT(*) AS cnt FROM Participant P1 JOIN Event_Participant VEP1 ON P1.PID = VEP1.PID JOIN Event E1 ON VEP1.EID = E1.EID WHERE E1.EName = 'Megaevent' GROUP BY P1.CName ) AS subquery)");
                    System.out.println("College");
                    System.out.println("-------");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;

                case 9: // Name of the college with the largest number of participants overall
                    rs = stmt.executeQuery("SELECT P.CName FROM Participant P JOIN Event_Participant VEP ON P.PID = VEP.PID GROUP BY P.CName HAVING COUNT(*) = ( SELECT MAX(cnt) FROM ( SELECT COUNT(*) AS cnt FROM Participant P1 JOIN Event_Participant VEP1 ON P1.PID = VEP1.PID GROUP BY P1.CName ) AS subquery)");
                    System.out.println("College");
                    System.out.println("-------");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;

                case 10: // Name of the department with the largest number of volunteers in  all the events which has at least one participant from "IITB"   
                    rs = stmt.executeQuery("WITH DeptCounts AS ( SELECT S.Dept, COUNT(*) AS deptCount FROM Student S JOIN Volunteer V ON S.Roll = V.Roll JOIN Student_Event SE ON S.Roll = SE.Roll JOIN Event E ON SE.EID = E.EID JOIN Event_Participant VEP ON E.EID = VEP.EID JOIN Participant P ON VEP.PID = P.PID WHERE P.CName = 'IITB' GROUP BY S.Dept ) SELECT Dept FROM DeptCounts WHERE deptCount = (SELECT MAX(deptCount) FROM DeptCounts)");
                    System.out.println("Department");
                    System.out.println("----------");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1));
                    }
                    break;

                case 11: // Roll number and name of all the students who are managing the event <input>
                    System.out.println("Enter event name:");
                    String eventname = input.next();
                    rs = stmt.executeQuery("SELECT S.Roll, S.Name FROM Student S, Student_Event SE, Event E WHERE S.Roll = SE.Roll AND SE.EID = E.EID AND E.EName = '" + eventname + "'");
                    System.out.println("\nRoll\tName");
                    System.out.println("----\t----");
                    while(rs.next())
                    {
                        System.out.println(rs.getString(1) + "\t" + rs.getString(2));
                    }
                    break;

                default:
                    System.out.println("Invalid choice");
                    break;
            }
            System.out.println("\n***");
            System.out.println("Do you want to re-query? (y/n)");
            String cont = input.next();
            if (cont.equals("n"))
            {
                break;
            }
            System.out.print("\033[H\033[2J");
        }

        // Close the database connection
        conn.close();
        // Close the scanner
        input.close();

        System.out.println("\nGoodbye!");
        System.out.println("Author: Prasanna Paithankar (21CS30065)");
    }
}
        