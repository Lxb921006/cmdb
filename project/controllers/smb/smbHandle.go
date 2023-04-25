package smb

import (
	"os/exec"
)

type SmbHandle struct {
	User      string
	PassWd    string
	Path      string
	ShareName string
	IsWrite   string
	Uid       []uint
}

type Option func(*SmbHandle)

func (sh *SmbHandle) AddSmbUser() (err error) {
	// cmd := fmt.Sprintf("%s %s %s %s %s %s", AddSmbUserScript, sh.User, sh.PassWd, sh.ShareName, sh.Path, sh.IsWrite)
	// out, err := exec.Command("/bin/bash", "-c", cmd).Output() ubuntu
	_, err = exec.Command("sh", AddSmbUserScript, sh.User, sh.PassWd, sh.ShareName, sh.Path, sh.IsWrite).Output()
	if err != nil {
		return
	}

	return
}

func (sh *SmbHandle) DelSmbUser() (err error) {
	_, err = exec.Command("sh", DelSmbUserScript, sh.User, sh.ShareName).Output()
	if err != nil {
		return
	}

	return
}

func (sh *SmbHandle) UpdateSmbUser() (err error) {
	_, err = exec.Command("sh", UpdateSmbUserScript, sh.User, sh.PassWd, sh.ShareName, sh.Path, sh.IsWrite).Output()
	if err != nil {
		return
	}

	return
}

func CallAll(params ...string) Option {
	return func(sh *SmbHandle) {
		sh.User = params[0]
		sh.PassWd = params[1]
		sh.Path = params[2]
		sh.ShareName = params[3]
		sh.IsWrite = params[4]
	}
}

func CallDel(params ...string) Option {
	return func(sh *SmbHandle) {
		sh.User = params[0]
		sh.ShareName = params[1]
	}
}

func NewSmbHandle(options ...Option) *SmbHandle {
	s := &SmbHandle{}
	for _, option := range options {
		option(s)
	}

	return s
}
