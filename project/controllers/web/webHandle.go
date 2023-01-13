package web

import (
	"errors"
	"os/exec"
)

type WebHandle struct {
	Path string
}

func (wh *WebHandle) CreateLog() (err error) {
	err = wh.ExecuteCmd(CreateLogScript)
	if err != nil {
		return
	}
	return
}

func (wh *WebHandle) ClearCache() (err error) {
	err = wh.ExecuteCmd(ClearCacheScript)
	if err != nil {
		return
	}
	return
}

func (wh *WebHandle) ExecuteCmd(cmd string) (err error) {
	out, err := exec.Command("sh", cmd, wh.Path).Output()
	if err != nil {
		return errors.New(string(out))
	}
	return
}

func NewWebHandle(path string) *WebHandle {
	return &WebHandle{
		Path: path,
	}
}
