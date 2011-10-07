SUBDIRS = dissections-cpp dissections-clojure spherical_bitrade_generator

.PHONY: subdirs $(SUBDIRS)

subdirs: $(SUBDIRS)

$(SUBDIRS):
	 $(MAKE) -C $@

dissections-cpp: spherical_bitrade_generator

clean :
	-for d in $(SUBDIRS); do (cd $$d; $(MAKE) clean ); done

