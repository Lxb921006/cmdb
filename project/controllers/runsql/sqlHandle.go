package runsql

import (
	"os/exec"
	"path/filepath"
	"strings"
)

type SqlHandle struct {
	SqlContents string `form:"sql" binding:"required"`
	Project     string `form:"project" binding:"required"`
	DbType      string `form:"dbType" binding:"required"`
}

func (s SqlHandle) RunIntranetSqlScript() (data string) {
	if strings.HasSuffix(s.SqlContents, ".sql") {
		out, _ := exec.Command("sh", IntranetSqlScript, s.Project+"-"+s.DbType, filepath.Join(Fp, s.SqlContents), "5").Output()
		return string(out)
	} else {
		out, _ := exec.Command("sh", IntranetSqlScript, s.Project+"-"+s.DbType, s.SqlContents, "7").Output()
		return string(out)
	}
}
