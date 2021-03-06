const pool = require("../utils/db.js");
const person_model = require("./person_model");
const project_model = require("./project_model");

async function getIssue(issue_id){
  return new Promise(async function(res, rej){
    try {
      conn = await pool.getConnection();
      sql = "SELECT * FROM Issues WHERE issue_id = ?";
      await conn.query(sql, [issue_id], function(err, results, fields){
        if (results[0]){
          res(results[0]);
        }else {
          console.log("Issue not found");
          res(null);
        }
      });
      conn.release();
    }catch (err){
      rej(err);
    }
 });
}

// add a long description to issue
async function updateDescription(issue_id, description){
  try{
    conn = await pool.getConnection();
    sql_desc = "UPDATE Issues SET issue_description = ? WHERE issue_id = ?";
    await conn.query(sql_desc, [description, issue_id], function(err, results, fields){
      if (err){
        console.log("Error with query");
      }
    });
    conn.release();
  }catch(err){
    throw(err);
  }
}

async function updateProgress(issue_id, progress){
  try{
    conn = await pool.getConnection();
    sql_progress = "UPDATE Issues SET progress = ? WHERE issue_id = ?";
    await conn.query(sql_progress, [progress, issue_id], function(err, results, fields){
      if (err){
        console.log("Error with query");
      }
    });
    conn.release();
  }catch (err){
    throw(err);
  }
}

async function changePriority(issue_id, priority){
  try{
    conn = await pool.getConnection();
    sql_prio = "UPDATE Issues SET priority = ? WHERE issue_id = ?";
    await conn.query(sql_prio, [priority, issue_id], function(err, results, fields){
      if (err){
        console.log("Error with query");
      }
    });
    conn.release();
  }catch (err){
    throw(err);
  }
}


module.exports = {

  //create new issue
  //username passed as argument, or maybe query it here
  async createIssue(username, summary, person_id, assigned_to, id_date, project_id, status){
    try {
      conn = await pool.getConnection();
      let date = new Date().toISOString().slice(0, 10).replace("T", " ");
      sql = "INSERT INTO Issues (issue_summary, identified_by_person_id, identified_date, related_project, assigned_to, issue_status, created_on, created_by, modified_on, modified_by)";
      sql += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
      await conn.query(sql, [summary, person_id, id_date, project_id, assigned_to, status, date, username, date, username]);
      conn.release();
      console.log("Issue created by: " + username);
    }catch (err) {
      throw err;
    }
  },

  getIssue: getIssue,

  async getIssuesByProject(project_id){
    return new Promise(async function(res,rej){
      try{
        conn = await pool.getConnection();
        sql = "SELECT * FROM Issues WHERE related_project = ?";
        await conn.query(sql, [project_id], function(err, results, fields){
          if (results){
            res(results);
          }else {
            res(null);
          }
        });
        conn.release();
      }catch (err){
        rej(err);
      }
    });
  },

  //Call when issue is finished, set it to closed and unassign user
  async closeIssue(issue_id, username, resolution_summary){
    try {
      conn = await pool.getConnection();
      if (resolution_summary){
        sql = "UPDATE Issues SET issue_status = 'Closed', resolution_summary = ? WHERE issue_id = ?";
        await conn.query(sql, [resolution_summary, issue_id], function(err, result, fields){
          if (err){
            console.log("Issue not closed properly");
          }
        });
      }else {
        sql = "UPDATE Issues SET issue_status = 'Closed' WHERE issue_id = ?";
        await conn.query(sql, [issue_id], function(err, result, fields){
          if (err){
            console.log("Issue not closed properly");
          }
        });
      }
      try {
        await person_model.assignIssue(username, 0);
        console.log("unassign worked");
      }catch (err){
        console.log("error unassigning");
      }
      /*
      const issue = getIssue(issue_id);
      sql = "SELECT username FROM People WHERE person_id = ?";
      await conn.query(sql, [issue.assigned_to], async function(err, results, fields){
        if (results.length == 1){
          await person_model.assignIssue(results[0].username, 0); //person should be assigned to nothing
        }else {
          console.log("Error unassigning person from issue");
        }
      });
      */
      conn.release();
    }catch (err){
      throw err;
    }
  },

  //edit an issue that is already created
  // need variable args?
  async updateIssue(issue_id, project_name, username, description, progress, priority){
    try{
      const date = new Date().toISOString().slice(0, 10).replace("T", " ");
      const project = await project_model.getProjectByName(project_name);
      if (project){
        if (description){
          await updateDescription(issue_id, description);
        }
        if (progress){
          await updateProgress(issue_id, progress);
        }
        if (priority){
          await changePriority(issue_id, priority);
        }
      }
      conn = await pool.getConnection();
      sql = "UPDATE Issues SET modified_on = ?, modified_by = ? WHERE issue_id = ?";
      await conn.query(sql, [date, username, issue_id], function(err, results, fields){
        if (err){
          console.log("error updating modified");
        }
      });
      conn.release();
    }catch(err){
      throw(err);
    }
  },

  //get all issues to show from a project
  async showAllIssues(project_id){
    return new Promise(async function(res, rej){
      try {
        conn = await pool.getConnection();
        sql = "SELECT * FROM Issues WHERE related_project = ?";
        await conn.query(sql, [project_id], function(err, results, fields){
          res(results);
        });
        conn.release();
      }catch (err) {
        rej(err);
      }
   });
  },

  //get all opened issues from project
  async showOpenIssues(project_id){
    return new Promise(async function(res, rej){
      try {
        conn = await pool.getConnection();
        sql = "SELECT * FROM Issues WHERE related_project = ? AND issue_status = 'open'";
        await conn.query(sql, [project_id], function(err, results, fields){
          res(results);
        });
      }catch (err){
        rej(err);
      }
    });
  },

  // get overdue issues by project
  async showOverdueIssues(project_id){
    return new Promise(async function(res, rej){
      try {
        conn = await pool.getConnection();
        let date = new Date().toISOString().slice(0, 10).replace("T", " ");
        sql = "SELECT * FROM Issues WHERE related_project = ? AND target_date < ?";
        await conn.query(sql, [project_id, date], function(err, results, fields){
          res(results);
        });
        conn.release();
      }catch (err){
        rej(err);
      }
    });
  },

  //Show some recent issues from different projects when user
  //clicks on issue tab from navbar
  async showRecentIssues(){
    return new Promise(async function(res, rej){
      try{
        conn = await pool.getConnection();
        sql = "SELECT * FROM Issues ORDER BY created_on DESC LIMIT 6";
        await conn.query(sql, function(err, results, fields){
          res(results);
        });
        conn.release();
      }catch (err){
        rej(err);
      }
    });
  }
};
