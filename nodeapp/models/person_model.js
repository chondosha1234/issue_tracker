const pool = require("../utils/db.js");
const auth = require("../utils/auth.js");

async function getUser(username){
  return new Promise(async function(res, rej){
  try {
    conn = await pool.getConnection();
    sql = "SELECT * FROM People WHERE username = ?";
    await conn.query(sql, [username], function(err, results, fields){
      if (err){
        console.err(err.message);
      }else {
        if(results.length == 1){
          res(results[0]);
        }else {
          res(null);
        }
      }
    });
   conn.release();
  }catch (err){
    rej(err);
  }
 });
}

module.exports = {

  //get info about one user
  getUser: getUser,

  //list all users
  async listUsers(){
    return new Promise(async function(res, rej){
      try{
        conn = await pool.getConnection();
        sql = "SELECT * FROM People";
        await conn.query(sql, [], function(err, results, fields){
          res(results);
        });
      }catch (err){
        rej(err);
      }
    });
  },

  // matches password of user with password argument
  async areValidCredentials(username, password){
    return new Promise(async function(res, rej){
    try {
      conn = await pool.getConnection();
      sql = "SELECT person_password FROM People WHERE username = ?";
      await conn.query(sql, [username], function(err, results, fields){
        if (err){
          console.error(err.message);
        }else {
          if (results.length == 1 && results[0].person_password === password){
            res(true);
          }else {
            res(false);
          }
        }
      });
      conn.release();
    } catch (err){
      rej(err);
    }
   });
  },

  //create user
  async createPerson(person_name, email, person_role, username, password){
    try {
      conn = await pool.getConnection();
      let date = new Date().toISOString().slice(0, 10).replace('T', ' ');
      sql = "INSERT INTO People (person_name, email, person_role, username, person_password, created_on, created_by, modified_on, modified_by)";
      sql += " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
      await conn.query(sql, [person_name, email, person_role, username, password, date, person_name, date, person_name]);
      conn.release();
      console.log("User created: " + username);
    }catch (err) {
      throw err;
    }
  },

  //assign project to user
  async assignIssue(username, issue, project){
    try {
      conn = await pool.getConnection();
      if (project.project_id === issue.related_project){
        sql = "UPDATE People SET assigned_issue = ? WHERE username = ?";
        await conn.query(sql, [issue.issue_id, username]);
        sql = "UPDATE Issues SET assigned_to = ? WHERE issue_id = ?";
        await conn.query(sql, [username, issue.issue_id]);
        const user = getUser(username);
      }else {
        console.log("Project doesnt exist");
      }
      conn.release();
      if (user.assigned_issue === 0){
        console.log("User: " + username + "now is unassigned.");
      }else {
        console.log("User: " + username + " now assigned to project: " + issue.issue_id);
      }
    }catch (err){
      throw err;
    }
  }
};
