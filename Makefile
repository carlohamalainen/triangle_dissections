SUBDIRS = dissections-cpp spherical_bitrade_generator

.PHONY: subdirs $(SUBDIRS)

subdirs: $(SUBDIRS)

$(SUBDIRS):
	 $(MAKE) -C $@

dissections-cpp: spherical_bitrade_generator
