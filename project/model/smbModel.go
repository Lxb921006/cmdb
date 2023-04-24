package model

import "github.com/Lxb921006/cmdb/project/dao"

type Tabler interface {
	TableName() string
}

type SmbModel struct {
	ID        uint   `gorm:"primaryKey" json:"id"`
	Name      string `gorm:"not null" json:"name"`
	ShareName string `gorm:"not null" json:"shareName"`
}

func (smb *SmbModel) TableName() string {
	return "smbServe_smbusermodel"
}

func (smb *SmbModel) GetSmbUsers(uid []uint) (smbUser []SmbModel, err error) {
	if err = dao.DB.Find(&smbUser, uid).Error; err != nil {
		return
	}

	return
}

func (smb *SmbModel) DelSmbUsers(uid []uint) (err error) {
	tx := dao.DB.Begin()

	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
		}
	}()

	if err = tx.Where("id IN ?", uid).Unscoped().Delete(&SmbModel{}).Error; err != nil {
		tx.Rollback()
		return
	}

	return
}
