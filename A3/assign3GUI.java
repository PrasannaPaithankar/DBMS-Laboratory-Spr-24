/*
 *  Author: Prasanna Paithankar (21CS30065)
 *  Date: 30/08/2021
 *  Course: Database Management Systems Lab
 *  File: assign3.java
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

// Class to create GUI for SQL queries
public class assign3GUI extends JFrame 
{
    private JTextArea resultArea;
    private JTextArea header;
    private JTextField input;

    // array to store queries
    private String[] queries = {"1. Roll number and name of all the students who are managing the \"Megaevent\"", "2. Roll number and name of all the students who are managing the \"Megaevent\" as an \"Secretary\"", "3. Name of all participants from the college \"IITB\" in \"Megaevent\"", "4. Name of all colleges who have at least one participant in \"Megaevent\"", "5. Name of all events which is managed by a \"Secretary\"", "6. Name of all the \"CSE\" department student volunteers of \"Megaevent\"", "7. Name of all the events which have at least one volunteer from \"CSE\"", "8. Name of the college with the largest number of participants in \"Megaevent\"", "9. Name of the college with the largest number of participants overall", "10. Name of the department with the largest number of volunteers in  all the events which has at least one participant from \"IITB\"", "11. Roll number and name of all the students who are managing the <input event below>"};

    // Constructor to create GUI
    public assign3GUI() 
    {
        setTitle("PostgreSQL Query GUI");
        // setSize(700, 700);
        // full screen
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        setResizable(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create components
        header = new JTextArea(4, 20);
        header.setMargin(new Insets(0, 0, 2, 0));
        header.setFont(new Font("Arial", Font.BOLD, 15));
        header.setText("Welcome to the JDBC Query Processor!\n\nClick on a button to execute the corresponding SQL query.");
        header.setEditable(false);
        JPanel buttonPanel = new JPanel(new GridLayout(0, 1, 10, 10));
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(10, 5, 0, 0));
        // set appropriate size for resultArea
        resultArea = new JTextArea(20, 25);
        resultArea.setEditable(false);
        resultArea.setFont(new Font("Arial", Font.PLAIN, 16));
        resultArea.setMargin(new Insets(10, 40, 10, 10));
        input = new JTextField(20);
        input.setFont(new Font("Arial", Font.PLAIN, 16));
        input.setMargin(new Insets(10, 40, 10, 10));


        // Add buttons for SQL queries
        for (int i = 1; i <= 11; i++) 
        {
            JButton queryButton = new JButton(queries[i - 1]);
            queryButton.setSize(new Dimension(10, 50));
            queryButton.setFont(new Font("Arial", Font.BOLD, 11));
            queryButton.setHorizontalAlignment(SwingConstants.LEFT);
            queryButton.addActionListener(new QueryButtonListener(i));
            buttonPanel.add(queryButton);
        }

        // Add components to the frame
        add(header, BorderLayout.NORTH);
        add(buttonPanel, BorderLayout.WEST);
        add(resultArea, BorderLayout.EAST);
        add(input, BorderLayout.SOUTH);
    }

    private class QueryButtonListener implements ActionListener 
    {
        private int queryNumber;

        public QueryButtonListener(int queryNumber) 
        {
            this.queryNumber = queryNumber;
        }

        @Override
        public void actionPerformed(ActionEvent e) 
        {
            // Execute SQL query based on the button clicked
            String query = getSQLQuery(queryNumber);
            // pass query and query number to executeQuery
            executeQuery(query, queryNumber);
        }
    }

    private String getSQLQuery(int queryNumber) 
    {
        // Replace this with your SQL queries
        switch (queryNumber) 
        {
            case 1:
                return "SELECT S.Roll, S.Name FROM Student S, Student_Event SE, Event E WHERE S.Roll = SE.Roll AND SE.EID = E.EID AND E.EName = 'Megaevent'";
            case 2:
                return "SELECT S.Roll, S.Name FROM Student S, Student_Event SE, Event E, Role R WHERE S.Roll = SE.Roll AND SE.EID = E.EID AND E.EName = 'Megaevent' AND S.RID = R.RID AND R.Rname = 'Secretary'";
            case 3:
                return "SELECT P.Name FROM Participant P, Event_Participant VEP, Event E WHERE P.PID = VEP.PID AND VEP.EID = E.EID AND E.EName = 'Megaevent' AND P.CName = 'IITB'";
            case 4:
                return "SELECT DISTINCT P.CName FROM Participant P, Event_Participant VEP, Event E WHERE P.PID = VEP.PID AND VEP.EID = E.EID AND E.EName = 'Megaevent'";
            case 5:
                return "SELECT E.EName FROM Event E, Student S, Student_Event SE, Role R WHERE E.EID = SE.EID AND SE.Roll = S.Roll AND S.RID = R.RID AND R.Rname = 'Secretary'";
            case 6:
                return "SELECT S.Name FROM Student S, Volunteer V, Event E, Student_Event SE WHERE S.Roll = V.Roll AND V.EID = E.EID AND E.EName = 'Megaevent' AND S.Dept = 'CSE' AND S.Roll = SE.Roll AND SE.EID = E.EID";
            case 7:
                return "SELECT E.EName FROM Event E, Student S, Volunteer V WHERE E.EID = V.EID AND V.Roll = S.Roll AND S.Dept = 'CSE'";
            case 8:
                return "SELECT P.CName FROM Participant P JOIN Event_Participant VEP ON P.PID = VEP.PID JOIN Event E ON VEP.EID = E.EID WHERE E.EName = 'Megaevent' GROUP BY P.CName HAVING COUNT(*) = ( SELECT MAX(cnt) FROM ( SELECT COUNT(*) AS cnt FROM Participant P1 JOIN Event_Participant VEP1 ON P1.PID = VEP1.PID JOIN Event E1 ON VEP1.EID = E1.EID WHERE E1.EName = 'Megaevent' GROUP BY P1.CName ) AS subquery)";
            case 9:
                return "SELECT P.CName FROM Participant P JOIN Event_Participant VEP ON P.PID = VEP.PID GROUP BY P.CName HAVING COUNT(*) = ( SELECT MAX(cnt) FROM ( SELECT COUNT(*) AS cnt FROM Participant P1 JOIN Event_Participant VEP1 ON P1.PID = VEP1.PID GROUP BY P1.CName ) AS subquery)";
            case 10:
                return "WITH DeptCounts AS ( SELECT S.Dept, COUNT(*) AS deptCount FROM Student S JOIN Volunteer V ON S.Roll = V.Roll JOIN Student_Event SE ON S.Roll = SE.Roll JOIN Event E ON SE.EID = E.EID JOIN Event_Participant VEP ON E.EID = VEP.EID JOIN Participant P ON VEP.PID = P.PID WHERE P.CName = 'IITB' GROUP BY S.Dept ) SELECT Dept FROM DeptCounts WHERE deptCount = (SELECT MAX(deptCount) FROM DeptCounts)";

            default:
                return "";
        }
    }

    private void executeQuery(String query, int queryNumber) 
    {
        // Connect to the database
        String jdbcURL = "jdbc:postgresql://localhost:5432/prasanna";
        String username = "prasanna";
        String password = "prasanna";

        try 
        {
            Connection connection = DriverManager.getConnection(jdbcURL, username, password);
            Statement statement = connection.createStatement();
            ResultSet resultSet = null;
            if (queryNumber != 11)
            {
                resultSet = statement.executeQuery(query);
            }

            // Display results in the text area
            resultArea.setText("");

            if (queryNumber <=2)
            {
                resultArea.append("Roll\tName\n----\t----\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\t" + resultSet.getString(2) + "\n");
                }
            }
            else if (queryNumber == 3)
            {
                resultArea.append("Name\n----\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 4)
            {
                resultArea.append("College\n-------\n");
                while (resultSet.next()) {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 5)
            {
                resultArea.append("Event\n-----\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 6)
            {
                resultArea.append("Name\n----\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 7)
            {
                resultArea.append("Event\n-----\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 8)
            {
                resultArea.append("College\n-------\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 9)
            {
                resultArea.append("College\n-------\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 10)
            {
                resultArea.append("Dept\n----\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\n");
                }
            }
            else if (queryNumber == 11)
            {
                resultSet = statement.executeQuery("SELECT S.Roll, S.Name FROM Student S, Student_Event SE, Event E WHERE S.Roll = SE.Roll AND SE.EID = E.EID AND E.EName = '" + input.getText() + "'");    
                resultArea.append("Roll\tName\n----\t----\n");
                while (resultSet.next()) 
                {
                    resultArea.append(resultSet.getString(1) + "\t" + resultSet.getString(2) + "\n");
                }
            }

            // Close resources
            resultSet.close();
            statement.close();
            connection.close();
        } 
        catch (Exception ex) 
        {
            resultArea.setText("Error executing query: " + ex.getMessage());
        }
    }

    public static void main(String[] args) 
    {
        // Run the GUI on the event dispatch thread
        javax.swing.SwingUtilities.invokeLater(new Runnable() 
        {
            public void run() {
                new assign3GUI().setVisible(true);
            }
        });
    }
}